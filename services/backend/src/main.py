from typing import Annotated
from fastapi import Depends, FastAPI, Response, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import functools
#from sqlalchemy import create_engine
from sqlmodel import create_engine, select, Session
from sqlalchemy.engine import URL
import os

import rss
import models

def env_or_error(variable: str):
    value: str = os.getenv(variable)
    if value:
        return value
    raise ValueError(f"Environment variable '{variable}' required but not found.")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

url = URL.create(
    drivername=os.environ.get("DB_DRIVER", "postgresql"),
    username=env_or_error("DB_USERNAME"),
    host=env_or_error("DB_HOST"),
    database=env_or_error("DB_NAME"),
    password=os.getenv("DB_PASSWORD"),
    # There is the caveat that you must specify the port if not using
    # a UNIX socket, but the way to fix that would be to check if the
    # host was a actual file, which right now is too much to justify.
    port=os.getenv("DB_PORT")
)

RSS_TITLE: str = env_or_error("RSS_TITLE")
RSS_BASE_LINK: str = env_or_error("RSS_LINK")
RSS_DESC: str = env_or_error("RSS_DESCRIPTION")

# Until OIDC is implemented, this will be used for
# privileged requests. Afterwards can be for recovery
RECOVERY_TOKEN: str | None = os.getenv("RECOVERY_TOKEN")

ENGINE = create_engine(url, echo=True)
models.db_setup(ENGINE)

# This will eventually be replaced with OIDC to integrate with the
# rest of it all, but just so I can post on the devlog for now
def verify_token(authorization: Annotated[str, Header()] = None):
    if RECOVERY_TOKEN is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No auth methods allowed.")
    elif authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided.")
    auth_parts: list[str] = authorization.split(" ")
    if auth_parts[0].lower() != "bearer" or len(auth_parts) < 2:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth method.")
    if auth_parts[1] != RECOVERY_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")


@app.get("/")
def home():
    return "Hello, World!"

@app.get("/devlog")
def get_devlog():
    with Session(ENGINE) as db:
        statement = select(models.DevlogEntry).order_by(models.DevlogEntry.published.desc())
        results = db.exec(statement)
        return list(results)

@app.post("/devlog", dependencies=[Depends(verify_token)])
def post_devlog(entry: models.DevlogEntry, authorization: Annotated[str | None, Header()] = None):
    with Session(ENGINE) as db:
        print(db.add(entry))
        print(db.commit())
        db.refresh(entry)
    return entry

@app.get("/devrss")
def devrss():
    with Session(ENGINE) as db:
        statement = select(models.DevlogEntry).order_by(models.DevlogEntry.published.desc())
        results = db.exec(statement)
        content = rss.generate_stream(RSS_TITLE, RSS_BASE_LINK, RSS_DESC, results)
    return Response(content=content, media_type="application/rss+xml")

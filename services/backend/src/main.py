import os
from typing import Annotated

import models
import rss
from config import CONFIG
from fastapi import Depends, FastAPI, Header, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.engine import URL

# from sqlalchemy import create_engine
from sqlmodel import Session, create_engine, select

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

url = URL.create(
    drivername=CONFIG.db.driver,
    username=CONFIG.db.username,
    host=CONFIG.db.host,
    database=CONFIG.db.database,
    password=CONFIG.db.password,
    # There is the caveat that you must specify the port if not using
    # a UNIX socket, but the way to fix that would be to check if the
    # host was a actual file, which right now is too much to justify.
    port=CONFIG.db.port,
)

# Until OIDC is implemented, this will be used for
# privileged requests. Afterwards can be for recovery
RECOVERY_TOKEN: str | None = os.getenv("RECOVERY_TOKEN")

ENGINE = create_engine(url, echo=True)
models.db_setup(ENGINE)


# This will eventually be replaced with OIDC to integrate with the
# rest of it all, but just so I can post on the devlog for now
def verify_token(authorization: Annotated[str, Header()] = None):
    if RECOVERY_TOKEN is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No auth methods allowed."
        )
    elif authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided."
        )
    auth_parts: list[str] = authorization.split(" ")
    if auth_parts[0].lower() != "bearer" or len(auth_parts) < 2:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth method."
        )
    if auth_parts[1] != RECOVERY_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token."
        )


@app.get("/")
def home():
    return "Hello, World!"


@app.get("/devlog")
def get_devlog():
    with Session(ENGINE) as db:
        statement = select(models.DevlogEntry).order_by(
            models.DevlogEntry.published.desc()
        )
        results = db.exec(statement)
        return list(results)


@app.post("/devlog", dependencies=[Depends(verify_token)])
def post_devlog(
    entry: models.DevlogEntry, authorization: Annotated[str | None, Header()] = None
):
    with Session(ENGINE) as db:
        print(db.add(entry))
        print(db.commit())
        db.refresh(entry)
    return entry


@app.get("/devrss")
def devrss():
    if CONFIG.rss is None:
        raise HTTPException(status_code=503, detail="RSS is not configured.")
    with Session(ENGINE) as db:
        statement = select(models.DevlogEntry).order_by(
            models.DevlogEntry.published.desc()
        )
        results = db.exec(statement)
        content = rss.generate_stream(
            CONFIG.rss.title, CONFIG.rss.link, CONFIG.rss.description, results
        )
    return Response(content=content, media_type="application/rss+xml")

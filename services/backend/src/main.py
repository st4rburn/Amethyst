import logging
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from starlette.middleware.sessions import SessionMiddleware

from . import auth, dependencies, models, rss
from .config import CONFIG
from .db import ENGINE

app = FastAPI(root_path=CONFIG.backend_path)

logging.warning((CONFIG.site_root.path))

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(CONFIG.site_root)],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=CONFIG.session_secret)

# Include routers
app.include_router(auth.router)


@app.get("/")
def home():
    return "Hello, World!"


@app.get("/devlog")
def get_devlog():
    with Session(ENGINE) as db:
        statement = select(models.DevlogEntry).order_by(
            models.DevlogEntry.published.desc()  # pyright: ignore [reportAttributeAccessIssue]
        )
        results = db.exec(statement)
        return list(results)


@app.post("/devlog", dependencies=[Depends(dependencies.verify_token)])
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
            models.DevlogEntry.published.desc()  # pyright: ignore [reportAttributeAccessIssue]
        )
        results = db.exec(statement)
        content = rss.generate_stream(
            CONFIG.rss.title, CONFIG.rss.link, CONFIG.rss.description, results
        )
    return Response(content=content, media_type="application/rss+xml")

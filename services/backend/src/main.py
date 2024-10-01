from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import os

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

engine = create_engine(url)

@app.get("/")
def home():
    return "Hello, World!"

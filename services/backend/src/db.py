from sqlalchemy.engine import URL
from sqlmodel import create_engine

from . import models
from .config import CONFIG

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

ENGINE = create_engine(url, echo=True)
models.db_setup(ENGINE)

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BLOB, LargeBinary, JSON, Enum, UniqueConstraint
from sqlalchemy.orm import declarative_base, Mapped
from typing import *
import enum
import slugify
import uuid

from config import *

class ChallengeDifficulty(enum.Enum):
    Beginner = 1
    Intermediate = 2
    Experienced = 3
    Advanced = 4
    Master = 5

class ChallengeType(enum.Flag):
    Miscellaneous = 0       # If there's no other type
    Steganography = 1
    Cryptography = 2
    Forensics = 4
    ReverseEngineering = 8  # rev
    RemoteEx = 16           # pwn
    WebEx = 32              # web
    Linux = 64


# https://coderpad.io/blog/development/sqlalchemy-with-postgresql/

# Can we automatically set up expiry and use it to call events?

# TODO: slugify titles on init

def new_machine_expiry():
    return datetime.datetime.now() + DEFAULT_MACHINE_EXPIRY

def new_id():
    # There won't be enough objects in any table for this to remotely become a problem
    return uuid.uuid4().bytes[:8]

Base = declarative_base()

# For anything in lists SQL: CREATE UNIQUE INDEX unique_list_position ON list_items (list_id, position);
# Ensures each position in a list is unique

class File(Base):
    __tablename__ = "files"

    id: Mapped[bytes]       = Column(BLOB(8),       primary_key=True, default=new_id)
    name: Mapped[str]       = Column(String(128),   nullable=False)
    content: Mapped[bytes]  = Column(LargeBinary,   nullable=False)
    md5: Mapped[bytes]      = Column(BLOB(16),      nullable=False)
    sha1: Mapped[bytes]     = Column(BLOB(16),      nullable=False)


class Challenge(Base):
    __tablename__ = "challenges"

    id: Mapped[bytes]           = Column(BLOB(8),       primary_key=True, default=new_id)
    title: Mapped[str]          = Column(String(128),   nullable=False, unique=True)    # Names should be unique for the sake of boring mode
    slug: Mapped[str]           = Column(String(128),   nullable=False, unique=True)
    description: Mapped[str]    = Column(String(2048),  nullable=False)
    position: Mapped[int]       = Column(Integer,       nullable=False)

    difficulty: Mapped[ChallengeDifficulty] = Column(Enum(ChallengeDifficulty), nullable=False)
    _type: Mapped[int]                      = Column(Integer,                   nullable=False, default=ChallengeType.Miscellaneous.value)

    episode_id: Mapped[bytes] = Column(BLOB(8), ForeignKey("episodes.id"), nullable=False)

    __table_args__ = (
        # Each challenge should have a unique position within the episode
        UniqueConstraint('episode_id', 'position', name='unique_challenge_position'),
    )

    @property
    def type(self) -> ChallengeType:
        return ChallengeType(self._type)
    @type.setter
    def type(self, new_type: ChallengeType) -> NoReturn:
        self._type = new_type.value


class Episode(Base):
    __tablename__ = "episodes"

    id: Mapped[bytes]           = Column(BLOB(8),       primary_key=True, default=new_id)
    title: Mapped[str]          = Column(String(128),   nullable=False)
    slug: Mapped[str]           = Column(String(128),   nullable=False)
    description: Mapped[str]    = Column(String(2048),  nullable=False)
    position: Mapped[int]       = Column(Integer,       nullable=False)

    release_date: Mapped[datetime.datetime] = Column(DateTime,  default=datetime.now,       nullable=False)
    season_id: Mapped[bytes]                = Column(BLOB(8),   ForeignKey("seasons.id"),   nullable=False)

    __table_args__ = (
        # Adding this constraint makes it possible to address by <base>/season/episode
        UniqueConstraint('season_id', 'slug', name='unique_episode_title'),
        # Each episode should have a unique position within the season
        UniqueConstraint('season_id', 'position', name='unique_episode_position'),
    )


class Season(Base):
    __tablename__ = "seasons"

    id: Mapped[bytes]           = Column(BLOB(8),       primary_key=True, default=new_id)
    title: Mapped[str]          = Column(String(128),   nullable=False, unique=True)
    slug: Mapped[str]           = Column(String(128),   nullable=False, unique=True)
    description: Mapped[str]    = Column(String(2048),  nullable=False)
    position: Mapped[int]       = Column(Integer,       nullable=False)

    # Calculate first and last challenge release


class User(Base):
    __tablename__ = "users"

    id: Mapped[bytes]       = Column(BLOB(8),       primary_key=True, default=new_id)
    username: Mapped[str]   = Column(String(32),    nullable=False)
    password: Mapped[bytes] = Column(BLOB(60),      nullable=False)
    email: Mapped[str]      = Column(String(64),    nullable=False)


class UserChallenge(Base):
    __tablename__ = "user_challenges"

    user_id: Mapped[bytes]                      = Column(BLOB(8),   ForeignKey("users.id"), primary_key=True)
    challenge_id: Mapped[bytes]                 = Column(BLOB(8),   ForeignKey("challenges.id"), primary_key=True)
    solve_date: Mapped[datetime.datetime]       = Column(DateTime,  default=datetime.now)
    machine: Mapped[bytes]                      = Column(BLOB(8),   ForeignKey("machines.id"))
    machine_expires: Mapped[datetime.datetime]  = Column(DateTime,  default=datetime.now)


# TODO: Make images table
# Probably import my EphermeralContainer class for this?
# - They will need to be stored in the database
# - Possibly a stripped version with a class for Docker arguments, which can be another table
#   - Images table, containers created from images and sometimes owned by users

class Image(Base):
    __tablename__ = "images"

    config_id: Mapped[bytes]    = Column(BLOB(8), primary_key=True, default=new_id)
    cpus: Mapped[int]           = Column(Integer, nullable=False)
    memory: Mapped[int]         = Column(Integer, nullable=False)

class Machine(Base):
    __tablename__ = "machines"

    # Also the container name when in hex
    machine_id: Mapped[bytes]   = Column(BLOB(8),   primary_key=True, default=new_id)
    owner: Mapped[bytes]        = Column(BLOB(8),   ForeignKey("users.id"))
    environment: Mapped[dict]   = Column(JSON,      nullable=False)
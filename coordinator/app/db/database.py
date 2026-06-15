from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore

DATABASE_URL = (
    "postgresql://fedforge:fedforge@localhost:5433/fedforge"
)

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)
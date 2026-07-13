from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore
from app.core.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_size = 30,
    max_overflow = 50,
    pool_timeout = 30,
    pool_pre_ping = True
)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)
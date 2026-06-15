from sqlalchemy import Column # type: ignore
from sqlalchemy import String # type: ignore
from sqlalchemy import DateTime # type: ignore

from app.db.base import Base

class Worker(Base):
    __tablename__ = "workers"

    worker_id = Column(
        String, primary_key = True
    )

    hostname = Column(
        String, nullable = False
    )

    ip = Column(
        String, nullable = False
    )

    status = Column(
        String, nullable = False
    )

    registered_at = Column(
        DateTime, nullable = False
    )

    last_seen = Column(
        DateTime, nullable = True
    )
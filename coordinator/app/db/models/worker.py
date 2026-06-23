from sqlalchemy import Column # type: ignore
from sqlalchemy import String # type: ignore
from sqlalchemy import DateTime # type: ignore
from sqlalchemy import Integer # type: ignore
from sqlalchemy import Enum #type: ignore

from app.models.enums import WorkerStatus
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

    cpu_cores = Column(
        Integer, nullable = False
    )

    memory_gb = Column(
        Integer, nullable = False
    )

    worker_version = Column(
        String, nullable = False
    )
    
    status = Column(
        Enum(WorkerStatus), nullable = False
    )

    registered_at = Column(
        DateTime(timezone = True), nullable = False
    )

    last_seen = Column(
        DateTime(timezone = True), nullable = True
    )
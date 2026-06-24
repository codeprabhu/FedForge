from uuid import uuid4
from sqlalchemy import Column, String, Float, DateTime # type: ignore
from app.db.base import Base

class WorkerMetric(Base):
    __tablename__ = "worker_metrics"

    metric_id = Column(
        String, primary_key = True, nullable = False
    )

    worker_id = Column(
        String, nullable = False
    )

    cpu_percent = Column(
        Float, nullable = False
    )

    memory_percent = Column(
        Float, nullable = False
    )

    disk_percent = Column(
        Float, nullable = False
    )

    recorded_at = Column(
        DateTime(timezone = True), nullable = False
    )
from sqlalchemy import Column # type: ignore
from sqlalchemy import String # type: ignore
from sqlalchemy import Enum # type: ignore
from sqlalchemy import DateTime # type: ignore
from sqlalchemy import JSON # type: ignore
from sqlalchemy import Text # type: ignore

from app.db.base import Base
from app.models.enums import TaskStatus, TaskType

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(
        String,
        primary_key=True
    )

    task_type = Column(
        Enum(TaskType),
        nullable=False
    )

    status = Column(
        Enum(TaskStatus),
        nullable=False
    )

    worker_id = Column(
        String,
        nullable=True
    )

    payload = Column(
        JSON,
        nullable=False
    )

    result = Column(
        JSON,
        nullable=True
    )

    error_message = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False
    )
    assigned_at = Column(
        DateTime(timezone = True),
        nullable=True
    )
    started_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )
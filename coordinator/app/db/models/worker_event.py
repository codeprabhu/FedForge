from uuid import uuid4
from app.models.enums import EventType

from sqlalchemy import Column # type: ignore
from sqlalchemy import String # type: ignore
from sqlalchemy import DateTime # type: ignore
from sqlalchemy import Enum # type: ignore
from app.db.base import Base

class WorkerEvent(Base):
    __tablename__ = "worker_events"

    event_id = Column(String, primary_key = True, 
                      default = lambda:str(uuid4()))
    worker_id = Column(String, nullable = False)
    event_type = Column(Enum(EventType), nullable = False)
    created_at = Column(DateTime(timezone = True), 
                        nullable = False)

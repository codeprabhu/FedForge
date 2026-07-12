from sqlalchemy import Column, Integer, String, DateTime, JSON # type: ignore
from datetime import datetime,UTC

from app.db.base import Base
class GlobalModel(Base):
    __tablename__ = "global_models"
    model_id = Column(Integer, primary_key = True)
    model_name = Column(String,nullable = False)
    version = Column(Integer, nullable = False)
    weights = Column(JSON, nullable = False)
    created_at = Column(DateTime, default = lambda: datetime.now(UTC))
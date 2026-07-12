from sqlalchemy import Column, String, Integer, DateTime # type: ignore
from datetime import datetime, UTC

from app.db.base import Base
class TrainingRound(Base):
    __tablename__ = "training_rounds"
    round_id = Column(String, primary_key = True)
    round_number = Column(Integer, nullable = False)
    model_name = Column(String, nullable=False)
    dataset_name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False,default=lambda: datetime.now(UTC))
    completed_at = Column(DateTime, nullable=True)
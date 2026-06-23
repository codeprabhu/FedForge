from app.db.database import engine
from app.db.base import Base
from app.db.models.task import Task

from app.db.models.worker import Worker
from app.db.models.worker_event import WorkerEvent

Base.metadata.create_all(bind = engine)
print("Tables created successfully")
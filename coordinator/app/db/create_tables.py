from coordinator.app.db.database import engine
from coordinator.app.db.base import Base

from coordinator.app.db.models.worker import Worker
from coordinator.app.db.models.worker_event import WorkerEvent

Base.metadata.create_all(bind = engine)
print("Tables created successfully")
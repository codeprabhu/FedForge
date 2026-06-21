from datetime import datetime, UTC
from app.repositories.worker_event_repository import WorkerEventRepository

class EventLogger:
    def __init__(self, event_repository:WorkerEventRepository):
        self.event_repository = event_repository

    def log(self, worker_id, event_type):
        event  = {
            "worker_id":worker_id,
            "event_type": event_type,
            "created_at": datetime.now(UTC)
        }
        self.event_repository.save(event)

    


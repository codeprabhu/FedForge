from uuid import uuid4
from datetime import datetime, UTC
from app.models.enums import WorkerStatus
class WorkerRegistry:
    def __init__(self, repository):
        self.repository = repository

    def register_worker(self, worker_data):
        worker_id = str(uuid4())

        worker = {
            **worker_data,
            "worker_id" : worker_id,
            "status" : WorkerStatus.REGISTERED,
            "registered_at" : datetime.now(UTC),
            "last_seen" : None,
        }
        self.repository.save(worker)
        return worker
    
    def get_all_workers(self):
        return list(self.repository.get_all())
    
    def get_worker(self, worker_id):
        return self.repository.get(worker_id)
    
    def heartbeat(self, worker_id):
        worker = self.repository.get(worker_id)

        if(worker is None):
            return None
        worker["last_seen"] = datetime.now(UTC)
        worker["status"] = WorkerStatus.ONLINE

        self.repository.update(worker)
        return worker

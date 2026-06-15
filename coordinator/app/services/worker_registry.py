from uuid import uuid4
from datetime import datetime, timedelta
from app.models.enums import WorkerStatus
class WorkerRegistry:
    def __init__(self):
        self.workers = {}

    def register_worker(self, worker_data):
        worker_id = str(uuid4())

        worker = {
            "worker_id" : worker_id,
            "status" : WorkerStatus.REGISTERED,
            "registered_at" : datetime.utcnow(),
            "last_seen" : None,
            **worker_data
        }
        self.workers[worker_id] = worker
        return worker
    
    def get_all_workers(self):
        return list(self.workers.values())
    
    def get_worker(self, worker_id):
        return self.workers.get(worker_id)
    
    def heartbeat(self, worker_id):
        worker = self.workers.get(worker_id)

        if(worker is None):
            return None
        worker["last_seen"] = datetime.utcnow()
        worker["status"] = WorkerStatus.ONLINE

        return worker

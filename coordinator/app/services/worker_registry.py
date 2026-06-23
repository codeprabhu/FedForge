from uuid import uuid4
from datetime import datetime, UTC

from app.models.enums import WorkerStatus, EventType
from app.db.models.worker import Worker
from app.models.worker import WorkerRegistrationRequest
class WorkerRegistry:
    def __init__(self, repository, event_logger):
        self.repository = repository
        self.event_logger = event_logger

    def register_worker(self, payload: WorkerRegistrationRequest):
        worker_id = str(uuid4())

        worker = Worker(
            worker_id = worker_id,
            hostname = payload.hostname,
            ip = payload.ip,
            cpu_cores = payload.cpu_cores,
            memory_gb = payload.memory_gb,
            worker_version = payload.worker_version,
            status=WorkerStatus.REGISTERED,
            registered_at=datetime.now(UTC),
            last_seen=None
        )
        self.repository.save(worker)
        self.event_logger.log(worker_id, EventType.WORKER_REGISTERED)
        return worker
    
    def get_all_workers(self):
        return self.repository.get_all()
    
    def get_worker(self, worker_id:str):
        return self.repository.get(worker_id)
    
    def heartbeat(self, worker_id:str):
        worker = self.repository.get(worker_id)

        if(worker is None):
            return None
        worker.last_seen = datetime.now(UTC)
        previous_status = worker.status
        worker.status = WorkerStatus.ONLINE

        if(previous_status != WorkerStatus.ONLINE):
            self.event_logger.log(worker.worker_id, EventType.WORKER_ONLINE)
        
        return worker

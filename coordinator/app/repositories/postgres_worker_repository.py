from coordinator.app.repositories.base import WorkerRepository
from coordinator.app.db.models.worker import Worker

class PostgresWorkerRepository(WorkerRepository):

    def __init__(self, db):
        self.db = db

    def _to_dict(self, worker):
        return {
            "worker_id": worker.worker_id,
            "hostname": worker.hostname,
            "ip": worker.ip,
            "cpu_cores": worker.cpu_cores,
            "memory_gb": worker.memory_gb,
            "worker_version": worker.worker_version,
            "status": worker.status,
            "registered_at": worker.registered_at,
            "last_seen": worker.last_seen
        }
    
    def save(self,worker_data):
        
        worker = Worker(
            worker_id = worker_data["worker_id"],
            hostname = worker_data["hostname"],
            ip = worker_data["ip"],
            cpu_cores = worker_data["cpu_cores"],
            memory_gb = worker_data["memory_gb"],
            worker_version = worker_data["worker_version"],
            status = worker_data["status"],
            registered_at = worker_data["registered_at"],
            last_seen = worker_data["last_seen"]
        )

        self.db.add(worker)
 
    def get(self, worker_id):

        worker = self.db.get(
            Worker, worker_id
        )

        if worker is None:
            return None
        return self._to_dict(worker)
    
    def get_all(self):
        workers = self.db.query(Worker).all()

        return [
            self._to_dict(worker)
            for worker in workers
            ]
    
    def update(self, worker_data):

        worker = self.db.get(
            Worker, worker_data["worker_id"]
        )

        if worker is None:
            return 
        
        worker.hostname = worker_data["hostname"]
        worker.ip = worker_data["ip"]
        worker.cpu_cores = worker_data["cpu_cores"]
        worker.memory_gb = worker_data["memory_gb"]
        worker.worker_version = worker_data["worker_version"]
        worker.status = worker_data["status"]
        worker.registered_at = worker_data["registered_at"]
        worker.last_seen = worker_data["last_seen"]

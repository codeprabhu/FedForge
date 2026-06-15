from app.repositories.base import WorkerRepository
from app.db.database import SessionLocal
from app.db.models.worker import Worker

class PostgresWorkerRepository(WorkerRepository):

    def _to_dict(self, worker):
        return {
            "worker_id": worker.worker_id,
            "hostname": worker.hostname,
            "ip": worker.ip,
            "status": worker.status,
            "registered_at": worker.registered_at,
            "last_seen": worker.last_seen
        }
    
    def save(self,worker_data):
        db = SessionLocal()
        
        worker = Worker(
            worker_id = worker_data["worker_id"],
            hostname = worker_data["hostname"],
            ip = worker_data["ip"],
            status = worker_data["status"],
            registered_at = worker_data["registered_at"],
            last_seen = worker_data["last_seen"]
        )

        db.add(worker)
        db.commit()

        db.close()
    
    def get(self, worker_id):
        db = SessionLocal()

        worker = db.get(
            Worker, worker_id
        )
        db.close()

        if worker is None:
            return None
        return self._to_dict(worker)
    
    def get_all(self):
        db = SessionLocal()
        workers = db.query(Worker).all()
        db.close()

        return [
            self._to_dict(worker)
            for worker in workers
            ]
    
    def update(self, worker_data):
        db = SessionLocal()

        worker = db.get(
            Worker, worker_data["worker_id"]
        )

        if worker is None:
            db.close()
            return 
        
        worker.hostname = worker_data["hostname"]
        worker.ip = worker_data["ip"]
        worker.status = worker_data["status"]
        worker.registered_at = worker_data["registered_at"]
        worker.last_seen = worker_data["last_seen"]

        db.commit()
        db.close()
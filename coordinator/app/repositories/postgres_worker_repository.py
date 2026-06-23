from app.repositories.base import Repository
from app.db.models.worker import Worker

class PostgresWorkerRepository(Repository):

    def __init__(self, db):
        self.db = db
    
    def save(self,worker):
        self.db.add(worker)
 
    def get(self, worker_id):

        worker = self.db.get(
            Worker, worker_id
        )
        return worker
    
    def get_all(self):
        workers = self.db.query(Worker).all()

        return workers
    
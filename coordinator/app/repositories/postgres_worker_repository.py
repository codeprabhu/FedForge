from app.repositories.base import WorkerRepository

class PostgresWorkerRepository(WorkerRepository):

    def save(self,worker):
        raise NotImplementedError
    
    def get(self, worker_id):
        raise NotImplementedError
    
    def get_all(self):
        raise NotImplementedError
    
    def update(self, worker):
        raise NotImplementedError
from coordinator.app.repositories.base import WorkerRepository

class MemoryWorkerRepository(WorkerRepository):
    def __init__(self):
        self.workers = {}

    def save(self, worker):
        self.workers[worker["worker_id"]] = worker

    def get(self, worker_id):
        return self.workers.get(worker_id)
    
    def get_all(self):
        return self.workers.values()
    
    def update(self, worker):
        self.workers[worker["worker_id"]] = worker
    
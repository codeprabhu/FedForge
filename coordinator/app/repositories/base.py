from abc import ABC, abstractmethod

class WorkerRepository(ABC):
    @abstractmethod
    def save(self, worker):
        pass
    
    @abstractmethod
    def get(self, worker_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, worker):
        pass
    
from app.repositories.memory_worker_repository import MemoryWorkerRepository
from app.services.worker_registry import WorkerRegistry

worker_repository = MemoryWorkerRepository()

worker_registry = WorkerRegistry(worker_repository)
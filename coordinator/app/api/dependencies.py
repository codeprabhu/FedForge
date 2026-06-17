from fastapi import Depends # type: ignore
from coordinator.app.db.session import get_db
from coordinator.app.repositories.postgres_worker_repository import PostgresWorkerRepository
from coordinator.app.services.worker_registry import WorkerRegistry

def get_worker_repository(
        db = Depends(get_db)
):
    return PostgresWorkerRepository(db)

def get_worker_registry(
        repository = Depends(
            get_worker_repository
        )
):
    return WorkerRegistry(repository)
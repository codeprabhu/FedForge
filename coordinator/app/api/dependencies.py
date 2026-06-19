from fastapi import Depends # type: ignore
from coordinator.app.db.session import get_db
from coordinator.app.repositories.postgres_worker_repository import PostgresWorkerRepository
from coordinator.app.services.worker_registry import WorkerRegistry
from coordinator.app.repositories.worker_event_repository import WorkerEventRepository
from coordinator.app.services.event_logger import EventLogger

def get_worker_repository(
        db = Depends(get_db)
):
    return PostgresWorkerRepository(db)

def get_worker_event_repository(db = Depends(get_db)):
    return WorkerEventRepository(db)

def get_event_logger(repository = Depends(get_worker_event_repository)):
    return EventLogger(repository)

def get_worker_registry(
        repository = Depends(
            get_worker_repository
        ), event_logger = Depends(
            get_event_logger
        )
):
    return WorkerRegistry(repository,event_logger)
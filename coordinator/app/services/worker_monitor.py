import asyncio
from datetime import datetime, timedelta, UTC

from coordinator.app.models.enums import WorkerStatus
from coordinator.app.core.config import (
    OFFLINE_THRESHOLD_SECONDS,
    HEARTBEAT_INTERVAL_SECONDS
)

from coordinator.app.db.unit_of_work import UnitOfWork
from coordinator.app.repositories.postgres_worker_repository import PostgresWorkerRepository
from coordinator.app.repositories.worker_event_repository import WorkerEventRepository
from coordinator.app.services.event_logger import EventLogger
from coordinator.app.models.enums import EventType

class WorkerMonitor:

    def __init__(self):
        self.running = True

    def stop(self):
        self.running = False

    async def monitor_loop(self):

        while self.running:
            now = datetime.now(UTC)

            with UnitOfWork() as db:

                repository = PostgresWorkerRepository(db)
                event_repository = WorkerEventRepository(db)
                event_logger = EventLogger(event_repository)

                for worker in repository.get_all():
                    if worker["last_seen"] is None:
                        continue
                    delta = now - worker["last_seen"]
                    if (now - worker["last_seen"]) > timedelta(
                        seconds=OFFLINE_THRESHOLD_SECONDS):
                        if worker["status"] != WorkerStatus.OFFLINE:
                            worker["status"] = WorkerStatus.OFFLINE
                    
                            repository.update(worker)
                         
                            event_logger.log(worker["worker_id"], EventType.WORKER_OFFLINE)
            await asyncio.sleep(
                HEARTBEAT_INTERVAL_SECONDS
            )
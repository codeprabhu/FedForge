import asyncio
from datetime import datetime, timedelta, UTC

from coordinator.app.models.enums import WorkerStatus
from coordinator.app.core.config import (
    OFFLINE_THRESHOLD_SECONDS,
    HEARTBEAT_INTERVAL_SECONDS
)

from coordinator.app.db.unit_of_work import UnitOfWork
from coordinator.app.repositories.postgres_worker_repository import PostgresWorkerRepository


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

                for worker in repository.get_all():

                    if worker["last_seen"] is None:
                        continue

                    if (
                        now - worker["last_seen"]
                    ) > timedelta(
                        seconds=OFFLINE_THRESHOLD_SECONDS
                    ):

                        worker["status"] = WorkerStatus.OFFLINE

                        repository.update(worker)

            await asyncio.sleep(
                HEARTBEAT_INTERVAL_SECONDS
            )
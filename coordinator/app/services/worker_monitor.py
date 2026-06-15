import asyncio
from datetime import datetime, timedelta
from app.models.enums import WorkerStatus
from app.core.config import *
class WorkerMonitor:
    def __init__(self, registry):
        self.registry = registry
        self.running = True
        
    def stop(self):
        self.running = False

    async def monitor_loop(self):
        while self.running:
            now = datetime.utcnow()

            for worker in self.registry.get_all_workers():
                if worker["last_seen"] is None:
                    continue

                if now - worker["last_seen"] > timedelta(seconds = OFFLINE_THRESHOLD_SECONDS):
                    worker["status"] = WorkerStatus.OFFLINE

            await asyncio.sleep(HEARTBEAT_INTERVAL_SECONDS)
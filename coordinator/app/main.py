from fastapi import FastAPI # type: ignore
from coordinator.app.api.workers import router as worker_router

from contextlib import asynccontextmanager
import asyncio

from coordinator.app.services.worker_monitor import WorkerMonitor

@asynccontextmanager
async def lifespan(app:FastAPI):
    monitor = WorkerMonitor()
    monitor_task = asyncio.create_task(
        monitor.monitor_loop()
    )

    print("Worker monitor Started")
    yield

    monitor.stop()
    monitor_task.cancel()
    print("Worker monitor stopped")


app = FastAPI(
    title = "FedForge Coordinator",
    version = "0.1.0",
    lifespan = lifespan
)

app.include_router(worker_router)

@app.get("/")
async def root():
    return {
        "service" : "fedforge-coordinator",
        "status" : "online",
        "version" : "0.1.0"
    }


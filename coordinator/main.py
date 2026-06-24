from fastapi import FastAPI # type: ignore

from app.api.workers import router as worker_router
from app.api.tasks import router as task_router
from app.api.metrics import router as metrics_router

from contextlib import asynccontextmanager
import asyncio

from app.services.worker_monitor import WorkerMonitor
from app.db.create_tables import create_tables

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()

    monitor = WorkerMonitor()
    monitor_task = asyncio.create_task(
        monitor.monitor_loop()
    )
    yield

    monitor.stop()
    monitor_task.cancel()


app = FastAPI(
    title = "FedForge Coordinator",
    version = "0.1.0",
    lifespan = lifespan
)

app.include_router(worker_router)
app.include_router(task_router)
app.include_router(metrics_router)

@app.get("/")
async def root():
    return {
        "service" : "fedforge-coordinator",
        "status" : "online",
        "version" : "0.1.0"
    }


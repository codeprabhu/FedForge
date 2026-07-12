from fastapi import FastAPI # type: ignore

from app.api.workers import router as worker_router
from app.api.tasks import router as task_router
from app.api.metrics import router as metrics_router
from app.api.dashboard import router as dashboard_router
from app.api.log import router as log_router
from app.api.rounds import router as round_router


from contextlib import asynccontextmanager
import asyncio

from app.services.worker_monitor import WorkerMonitor
from app.services.round_scheduler import RoundScheduler
from app.db.create_tables import create_tables

from fastapi.middleware.cors import CORSMiddleware # type:ignore

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()

    scheduler = RoundScheduler()
    scheduler_task = asyncio.create_task(scheduler.scheduler_loop())
    
    monitor = WorkerMonitor()
    monitor_task = asyncio.create_task(monitor.monitor_loop())
    yield

    monitor.stop()
    monitor_task.cancel()


app = FastAPI(
    title = "FedForge Coordinator",
    version = "0.1.0",
    lifespan = lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(worker_router)
app.include_router(task_router)
app.include_router(metrics_router)
app.include_router(dashboard_router)
app.include_router(log_router)
app.include_router(round_router)

@app.get("/")
async def root():
    return {
        "service" : "fedforge-coordinator",
        "status" : "online",
        "version" : "0.1.0"
    }


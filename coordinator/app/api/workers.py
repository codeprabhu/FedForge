from fastapi import APIRouter  # type: ignore
from app.models.worker import WorkerRegistrationRequest
from app.core.coordinator import *

router  = APIRouter()
worker_registry = worker_registry

@router.post("/workers/register")
def register_worker(payload : WorkerRegistrationRequest):
    worker = worker_registry.register_worker(
        payload.model_dump()
    )
    return worker

@router.get("/workers")
def get_workers():
    return worker_registry.get_all_workers()

@router.post("/workers/{worker_id}/heartbeat")
def heartbeat(worker_id:str):
    worker = worker_registry.heartbeat(worker_id)
    if worker is None:
        return {
            "error": "worker not found"
        }
    return {
        "status":"heartbeat recieved"
    }

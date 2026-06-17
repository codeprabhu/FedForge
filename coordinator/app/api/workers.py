from fastapi import APIRouter, Depends  # type: ignore
from coordinator.app.models.worker import WorkerRegistrationRequest
from coordinator.app.api.dependencies import get_worker_registry
from coordinator.app.services.worker_registry import WorkerRegistry

router  = APIRouter()

@router.post("/workers/register")
def register_worker(payload : WorkerRegistrationRequest,
                    worker_registry : WorkerRegistry = Depends(get_worker_registry)):
    worker = worker_registry.register_worker(
        payload.model_dump()
    )
    return worker

@router.get("/workers")
def get_workers(worker_registry : WorkerRegistry= Depends(get_worker_registry)):
    return worker_registry.get_all_workers()

@router.post("/workers/{worker_id}/heartbeat")
def heartbeat(worker_id:str,
              worker_registry: WorkerRegistry = Depends(get_worker_registry)):
    worker = worker_registry.heartbeat(worker_id)
    if worker is None:
        return {
            "error": "worker not found"
        }
    return {
        "status":"heartbeat received"
    }

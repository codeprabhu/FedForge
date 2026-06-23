from fastapi import APIRouter, Depends  # type: ignore
from app.models.worker import WorkerRegistrationRequest
from app.api.dependencies import get_worker_registry
from app.services.worker_registry import WorkerRegistry
from fastapi import HTTPException # type: ignore

router  = APIRouter()

@router.post("/workers/register")
def register_worker(payload : WorkerRegistrationRequest,
                    worker_registry : WorkerRegistry = Depends(get_worker_registry)):
    worker = worker_registry.register_worker(payload)
    return worker

@router.get("/workers")
def get_workers(worker_registry : WorkerRegistry= Depends(get_worker_registry)):
    return worker_registry.get_all_workers()

@router.post("/workers/{worker_id}/heartbeat")
def heartbeat(worker_id:str,
              worker_registry: WorkerRegistry = Depends(get_worker_registry)):
    worker = worker_registry.heartbeat(worker_id)
    if worker is None:
        raise HTTPException(status_code = 404, detail = "Worker Not Found")
    return {"status":"heartbeat received"}

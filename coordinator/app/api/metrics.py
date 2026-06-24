from fastapi import APIRouter, Depends # type: ignore
from app.models.worker_metric import WorkerMetricsRequest
from app.api.dependencies import get_worker_metrics_registry
from app.services.metrics_registry import MetricsRegistry

router = APIRouter()

@router.post("/workers/{worker_id}/metrics")
def record_metrics(worker_id: str, payload: WorkerMetricsRequest,
                   registry: MetricsRegistry = Depends(get_worker_metrics_registry)):
    metric = registry.record_metrics(
        worker_id = worker_id,
        cpu_percent = payload.cpu_percent,
        memory_percent = payload.memory_percent,
        disk_percent = payload.disk_percent
    )
    return metric

@router.get("/workers/{worker_id}/metrics")
def get_metrics(worker_id : str, registry : MetricsRegistry = Depends(get_worker_metrics_registry)):
    return registry.get_worker_metrics(worker_id)

@router.get("/workers/{worker_id}/metrics/latest")
def get_latest_metrics(worker_id : str, registry: MetricsRegistry = Depends(get_worker_metrics_registry)):
    return registry.get_latest_metrics(worker_id)
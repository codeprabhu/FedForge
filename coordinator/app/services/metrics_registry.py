from uuid import uuid4
from datetime import datetime, UTC
from app.db.models.worker_metric import WorkerMetric

class MetricsRegistry:
    def __init__(self, repository):
        self.repository = repository

    def record_metrics(
        self,worker_id: str,cpu_percent: float,
        memory_percent: float,disk_percent: float):
        metric = WorkerMetric(
            metric_id = str(uuid4()),
            worker_id = worker_id,
            cpu_percent = cpu_percent,
            memory_percent = memory_percent,
            disk_percent = disk_percent,
            recorded_at = datetime.now(UTC)
        )
        self.repository.save(metric)
        return metric
    
    def get_metric(self, metric_id: str):
        return self.repository.get(metric_id)
    
    def get_worker_metrics(self, worker_id: str):
        return self.repository.get_by_worker(worker_id)
    
    def get_latest_metrics(self, worker_id: str):
        return self.repository.get_latest(worker_id)
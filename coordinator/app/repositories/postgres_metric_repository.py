from app.db.models.worker_metric import WorkerMetric

class PostgresWorkerMetricsRepository:
    def __init__(self,db):
        self.db = db

    def save(self, metric):
        self.db.add(metric)
        self.db.flush()

    def get(self, metric_id):
        return self.db.get(WorkerMetric, metric_id)
    
    def get_by_worker(self, worker_id):
        return (
            self.db.query(WorkerMetric).filter(
                WorkerMetric.worker_id == worker_id
            ).order_by(
                WorkerMetric.recorded_at.desc()
            ).all())
    
    def get_latest(self, worker_id):
        return (
            self.db.query(WorkerMetric).filter(
                WorkerMetric.worker_id == worker_id
            ).order_by(
                WorkerMetric.recorded_at.desc()
            ).first())
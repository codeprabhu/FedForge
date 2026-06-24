import time
import psutil
from runtime.background_service import BackgroundService
from models.worker_metric import WorkerMetrics
from exceptions.coordinator_unavailable_error import CoordinatorUnavailableError

class MetricsReporter(BackgroundService):
    def __init__(self, worker_client, interval_seconds):
        self.worker_client = worker_client
        self.interval_seconds = interval_seconds
        self.running = True

    def stop(self):
        self.running = False

    def run(self, worker_id):
        while(self.running):
            metrics = WorkerMetrics(
                cpu_percent=psutil.cpu_percent(),
                memory_percent=psutil.virtual_memory().percent,
                disk_percent=psutil.disk_usage("/").percent
            )

            try:
                self.worker_client.send_metrics(worker_id, metrics.model_dump())
            except CoordinatorUnavailableError:
                print("Coordinator Unavailable")

            time.sleep(self.interval_seconds)
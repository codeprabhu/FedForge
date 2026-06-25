import time
from runtime.background_service import BackgroundService
from exceptions.coordinator_unavailable_error import CoordinatorUnavailableError

class TaskPoller(BackgroundService):
    def __init__(self, worker_client, task_executor, interval_seconds):
        self.worker_client = worker_client
        self.task_executor = task_executor
        self.interval_seconds = interval_seconds
        self.running = True

    def stop(self):
        self.running = False

    def run(self, worker_id):
        while self.running:
            try:
                task = self.worker_client.get_next_task(worker_id)
                if task is None:
                    time.sleep(self.interval_seconds)
                    continue
                task_id = task["task_id"]

                self.worker_client.start_task(task_id)
                result = self.task_executor.execute(
                    task["task_type"], task["payload"])
                result = self.task_executor.execute(
                    task["task_type"], task["payload"])
                self.worker_client.complete_task(
                    task_id, result)

            except CoordinatorUnavailableError:
                    pass
            except Exception as error:
                try:
                    if task is not None:
                        self.worker_client.fail_task(task["task_id"], str(error))

                except Exception:
                    pass

                time.sleep(self.interval_seconds)
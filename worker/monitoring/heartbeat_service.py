import time
from runtime.background_service import BackgroundService
from exceptions.coordinator_unavailable_error import CoordinatorUnavailableError

class HeartbeatService(BackgroundService):
    def __init__(self, worker_client, interval_seconds):
        self.worker_client = worker_client
        self.interval_seconds = interval_seconds
        self.running = True

    def stop(self):
        self.running = False

    def run(self, worker_id):
        print("Heartbeat loop started.")
        while self.running:
            try:
                self.worker_client.heartbeat(worker_id)

            except CoordinatorUnavailableError:
                pass

            time.sleep(self.interval_seconds)

    
import time
class HeartbeatService:
    def __init__(self, worker_client, interval_seconds):
        self.worker_client = worker_client
        self.interval_seconds = interval_seconds
        self.running = True

    def stop(self):
        self.running = False

    def run(self, worker_id):
        print("Heartbeat loop started.")
        while self.running:
            self.worker_client.heartbeat(worker_id)
            print("Heartbeat Sent.")

            time.sleep(self.interval_seconds)

    
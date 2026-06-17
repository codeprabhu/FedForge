import socket
import os

from worker.config import WORKER_VERSION
class WorkerInfoProvider:
    def get_worker_info(self):
        return {
            "hostname": socket.gethostname(),
            "ip" : socket.gethostbyname(socket.gethostname()),
            "cpu_cores": os.cpu_count(),
            "memory_gb": 16,
            "worker_version": WORKER_VERSION
        }
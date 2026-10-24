import requests
from exceptions.coordinator_unavailable_error import CoordinatorUnavailableError
class WorkerClient:
    def __init__(self, base_url:str):
        self.base_url = base_url.rstrip("/")

    def register(self, worker_data: dict):
        try:
            response = requests.post(
                f"{self.base_url}/workers/register",
                json = worker_data, timeout=30
            )

            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            raise CoordinatorUnavailableError(
                "Coordinator Unavailable"
            ) from error
        
    def heartbeat(self, worker_id: str):
        try:
            response = requests.post(
                f"{self.base_url}/workers/{worker_id}/heartbeat", timeout=15
            )

            response.raise_for_status()

            return response.json()

        except requests.RequestException as error:

            raise CoordinatorUnavailableError(
                "Coordinator unavailable"
            ) from error
        
    def send_metrics(self, worker_id: str, metrics: dict):
        try:
            response = requests.post(
                f"{self.base_url}/workers/{worker_id}/metrics", json=metrics, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            raise CoordinatorUnavailableError("Coordinator Unavailable") from error
        
    def get_next_task(self, worker_id: str):
        try:
            response = requests.post(f"{self.base_url}/workers/{worker_id}/next-task", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            raise CoordinatorUnavailableError("Coordinator Unavailable") from error
        
    def start_task(self, task_id: str):
        try:
            response = requests.post(f"{self.base_url}/tasks/{task_id}/start", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            raise CoordinatorUnavailableError("Coordinator Unavailable") from error
        
    def complete_task(self, task_id: str, result: dict):
        try:
            response = requests.post(f"{self.base_url}/tasks/{task_id}/complete",
                json={"result": result}, timeout=120)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            raise CoordinatorUnavailableError("Coordinator unavailable") from error
        
    def fail_task(self, task_id: str, error_message: str):
        try:
            response = requests.post(f"{self.base_url}/tasks/{task_id}/fail",
                json={"error_message": error_message}, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            raise CoordinatorUnavailableError("Coordinator unavailable") from error
        
    def get_latest_model(self):
        try:
            response = requests.get(
                f"{self.base_url}/global-model/latest", timeout=60)
            response.raise_for_status()
            return response.json()
        
        except requests.RequestException as error:
            raise CoordinatorUnavailableError(
                "Coordinator Unavailable mbad bro"
            ) from error
        
    def get_model(self, version: int):
        try: 
            response = requests.get(
                f"{self.base_url}/global-model/{version}", timeout=60)
            response.raise_for_status()
            return response.json()
        
        except requests.RequestException as error:
            raise CoordinatorUnavailableError("Coordinator aint here bro") from error

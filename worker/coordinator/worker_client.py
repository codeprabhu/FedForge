import requests
from exceptions.coordinator_unavailable_error import CoordinatorUnavailableError
class WorkerClient:
    def __init__(self, base_url:str):
        self.base_url = base_url.rstrip("/")

    def register(self, worker_data: dict):
        try:
            response = requests.post(
                f"{self.base_url}/workers/register",
                json = worker_data
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
                f"{self.base_url}/workers/{worker_id}/heartbeat"
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
                f"{self.base_url}/workers/{worker_id}/metrics",json = metrics)
            response.raise_for_status
            return response.json()
        except requests.RequestException as error:
            raise CoordinatorUnavailableError("Coordinator Unavailable") from error
        

    def get_next_task(self, worker_id: str):
        try:
            response = requests.post(f"{self.base_url}/workers/{worker_id}/next-task")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            raise CoordinatorUnavailableError("Coordinator Unavailable") from error
        
    def start_task(self, task_id: str):
        try:
            response = requests.post(f"{self.base_url}/tasks/{task_id}/start")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            raise CoordinatorUnavailableError("Coordinator Unavailable") from error
        
    def complete_task(self, task_id: str, result: dict):
        try:
            response = requests.post(f"{self.base_url}/tasks/{task_id}/complete",
                json={"result": result})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            raise CoordinatorUnavailableError("Coordinator unavailable") from error
        

    def fail_task(self, task_id: str, error_message: str):
        try:
            response = requests.post(f"{self.base_url}/tasks/{task_id}/fail",
                json={"error_message": error_message})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            raise CoordinatorUnavailableError("Coordinator unavailable") from error
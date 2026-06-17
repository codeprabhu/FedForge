import requests
class WorkerClient:
    def __init__(self, base_url:str):
        self.base_url = base_url.rstrip("/")

    def register(self, worker_data: dict):
        response = requests.post(
            f"{self.base_url}/workers/register",
            json = worker_data
        )

        response.raise_for_status()
        return response.json()
    
    def heartbeat(self, worker_id : str):
        response = requests.post(
            f"{self.base_url}/workers/{worker_id}/heartbeat"
        )

        response.raise_for_status()
        return response.json()
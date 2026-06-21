import json
from pathlib import Path

from models.worker_identity import WorkerIdentity
from exceptions.identity_corrupted_error import IdentityCorruptedError

class IdentityStore:
    def __init__(self, path = "data/worker_identity.json"):
        self.path = Path(path)
    
    def exists(self):
        return self.path.exists()
    
    def save(self, identity: WorkerIdentity):
        self.path.parent.mkdir(
            parents = True,
            exist_ok=True
        )

        with open(self.path, "w") as file:
            json.dump(
                {
                    "worker_id":identity.worker_id
                },
                file, indent=4)
    
    def load(self):
        try:
            with open(self.path, "r") as file:
                data = json.load(file)

            return WorkerIdentity(
            worker_id=data["worker_id"]
            )
        except(KeyError, json.JSONDecodeError) as error:
            raise IdentityCorruptedError(
                "Worker Identity file is corrupted"
            ) from error
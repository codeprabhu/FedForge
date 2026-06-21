from models.worker_identity import WorkerIdentity
import requests
import random
import time

from core.config import (
    REGISTRATION_INITIAL_DELAY_SECONDS,
    REGISTRATION_MAX_DELAY_SECONDS,
    REGISTRATION_JITTER_FACTOR
)
class RegistrationService:
    def __init__(self, identity_manager, worker_client):
        self.identity_manager = identity_manager
        self.worker_client = worker_client

    def register_if_needed(self, worker_info: dict):
        if self.identity_manager.has_identity():
            print("Identity already Exists")
            return self.identity_manager.get_identity()
        print("No Identity Found")
        print("Registering Worker :)")
        response = self.register_with_retry(worker_info)
        identity = WorkerIdentity(worker_id=response["worker_id"])

        self.identity_manager.save_identity(identity)
        print("Worker Registered: ", identity.worker_id)
        return identity
    
    def register_with_retry(self, worker_info: dict):
        delay = (REGISTRATION_INITIAL_DELAY_SECONDS)
        while True:
            try:
                return self.worker_client.register(worker_info)
            except requests.ConnectionError:
                jitter = random.uniform(1-REGISTRATION_JITTER_FACTOR, 1+REGISTRATION_JITTER_FACTOR)
                sleep_time = delay * jitter

                print(f"Coordinator unavailable. "
                    f"Retrying in "
                    f"{sleep_time:.1f} seconds...")
                time.sleep(sleep_time)
                delay = min(delay*2, REGISTRATION_MAX_DELAY_SECONDS)
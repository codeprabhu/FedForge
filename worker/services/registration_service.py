from worker.models.worker_identity import WorkerIdentity
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
        response = self.worker_client.register(worker_info)
        identity = WorkerIdentity(worker_id=response["worker_id"])

        self.identity_manager.save_identity(identity)
        print("Worker Registered: ", identity.worker_id)
        return identity
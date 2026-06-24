from models.worker_identity import (
    WorkerIdentity
)


class IdentityManager:

    def __init__(
        self,
        store
    ):
        self.store = store

    def has_identity(self):

        return self.store.exists()

    def get_identity(self):

        return self.store.load()

    def save_identity(
        self,
        identity: WorkerIdentity
    ):

        self.store.save(identity)
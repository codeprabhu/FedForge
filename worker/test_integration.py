from worker.storage.identity_store import (
    IdentityStore
)

from worker.services.identity_manager import (
    IdentityManager
)

from worker.services.worker_client import (
    WorkerClient
)

from worker.services.registration_service import (
    RegistrationService
)


store = IdentityStore()

identity_manager = IdentityManager(
    store
)

client = WorkerClient(
    "http://localhost:8000"
)

registration_service = RegistrationService(
    identity_manager,
    client
)

identity = registration_service.register_if_needed(
    {
        "hostname": "worker-test",
        "ip": "127.0.0.1",
        "cpu_cores": 8,
        "memory_gb": 16,
        "worker_version": "1.0.0"
    }
)

print(identity)
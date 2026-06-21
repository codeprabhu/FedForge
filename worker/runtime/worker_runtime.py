from core.config import COORDINATOR_URL, HEARTBEAT_INTERVAL_SECONDS
from storage.identity_store import IdentityStore

from services.identity_manager import IdentityManager
from services.worker_client import WorkerClient
from services.registration_service import RegistrationService

from services.heartbeat_service import HeartbeatService
from services.worker_info_provider import WorkerInfoProvider

class WorkerRuntime:
    def run(self):
        store = IdentityStore()
        identity_manager = (IdentityManager(store))

        worker_client = WorkerClient(COORDINATOR_URL)
        registration_service = RegistrationService(identity_manager, worker_client)

        worker_info_provider = WorkerInfoProvider()
        hearbeat_service = HeartbeatService(worker_client, HEARTBEAT_INTERVAL_SECONDS)

        worker_info = worker_info_provider.get_worker_info()
        identity = registration_service.register_if_needed(worker_info)

        hearbeat_service.run(identity.worker_id)

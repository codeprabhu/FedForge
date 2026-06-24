import time
from runtime.service_runner import ServiceRunner

from core.config import COORDINATOR_URL, HEARTBEAT_INTERVAL_SECONDS
from storage.identity_store import IdentityStore

from identity.identity_manager import IdentityManager
from coordinator.worker_client import WorkerClient
from identity.registration_service import RegistrationService

from monitoring.heartbeat_service import HeartbeatService
from monitoring.worker_info_provider import WorkerInfoProvider

from monitoring.metrics_reporter import MetricsReporter
from core.config import METRICS_INTERVAL_SECONDS
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

        metrics_reporter = MetricsReporter(worker_client, METRICS_INTERVAL_SECONDS)

        runner = ServiceRunner()
        runner.start(hearbeat_service, identity.worker_id)
        runner.start(metrics_reporter, identity.worker_id)

        runner.wait()
        while True:
            time.sleep(1)
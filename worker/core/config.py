import os

COORDINATOR_URL = os.getenv(
    "COORDINATOR_URL",
    "http://localhost:8000"
)
WORKER_IDENTITY_PATH = os.getenv(
    "WORKER_IDENTITY_PATH",
    "worker_data/worker_identity.json",
)

HEARTBEAT_INTERVAL_SECONDS = int(
    os.getenv(
        "HEARTBEAT_INTERVAL_SECONDS",
        "30"
    )
)
TASK_POLL_INTERVAL_SECONDS = int(
    os.getenv(
        "TASK_POLL_INTERVAL_SECONDS",
        "10"
    )
)
WORKER_VERSION = "1.0.0"

REGISTRATION_INITIAL_DELAY_SECONDS = 1
REGISTRATION_MAX_DELAY_SECONDS = 60
REGISTRATION_JITTER_FACTOR = 0.2

METRICS_INTERVAL_SECONDS = 60

HIGGS_DATASET_URL = (
    os.getenv(
        "HIGGS_DATASET_URL",
        "https://archive.ics.uci.edu/ml/machine-learning-databases/00280/HIGGS.csv.gz",
    )
)
HIGGS_PREPROCESS_CHUNK_ROWS = int(os.getenv("HIGGS_PREPROCESS_CHUNK_ROWS", "100000"))
HIGGS_DATALOADER_WORKERS = int(os.getenv("HIGGS_DATALOADER_WORKERS", "0"))
# Keep local development rounds bounded. Set to 0 to train on the full dataset.
HIGGS_MAX_ROWS = int(os.getenv("HIGGS_MAX_ROWS", "100000"))

import os

HEARTBEAT_INTERVAL_SECONDS = 10
OFFLINE_THRESHOLD_SECONDS = 30
EVENT_LIMIT = 100

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://fedforge:fedforge@localhost:5433/fedforge")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

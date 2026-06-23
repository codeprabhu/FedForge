from enum import Enum

class WorkerStatus(str, Enum):
    REGISTERED = "REGISTERED"
    ONLINE  = "ONLINE"
    OFFLINE = "OFFLINE"
    TRAINING = "TRAINING"

class EventType(str, Enum):
    WORKER_REGISTERED = "WORKER_REGISTERED"
    WORKER_ONLINE = "WORKER_ONLINE"
    WORKER_OFFLINE = "WORKER_OFFLINE"

class TaskStatus(str, Enum):
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    ASSIGNED = "ASSIGNED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class TaskType(str, Enum):
    ECHO = "ECHO"
    TRAINING = "TRAINING"
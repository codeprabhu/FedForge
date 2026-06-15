from enum import Enum

class WorkerStatus(str, Enum):
    REGISTERED = "REGISTERED"
    ONLINE  = "ONLINE"
    OFFLINE = "OFFLINE"
    TRAINING = "TRAINING"
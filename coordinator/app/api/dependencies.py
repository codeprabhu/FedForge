from fastapi import Depends # type: ignore

from app.db.session import get_db

from app.repositories.postgres_worker_repository import PostgresWorkerRepository
from app.services.worker_registry import WorkerRegistry

from app.repositories.worker_event_repository import WorkerEventRepository
from app.services.event_logger import EventLogger

from app.repositories.postgres_task_repository import PostgresTaskRepository
from app.services.task_registry import TaskRegistry

from app.repositories.postgres_metric_repository import PostgresWorkerMetricsRepository
from app.services.metrics_registry import MetricsRegistry

from app.repositories.training_round_repository import TrainingRoundRepository
from app.repositories.global_model_repository import GlobalModelRepository
from app.services.global_model_manager import GlobalModelManager
from app.services.aggregation_service import AggregationService
from app.aggregation.strategies.fedavg_strategy import FedAvgStrategy
from app.services.round_manager import RoundManager

from app.services.dashboard_service import DashboardService

def get_worker_repository(
        db = Depends(get_db)
):
    return PostgresWorkerRepository(db)

def get_worker_event_repository(db = Depends(get_db)):
    return WorkerEventRepository(db)

def get_event_logger(repository = Depends(get_worker_event_repository)):
    return EventLogger(repository)

def get_worker_registry(
        repository = Depends(
            get_worker_repository
        ), event_logger = Depends(
            get_event_logger
        )
):
    return WorkerRegistry(repository,event_logger)

def get_task_repository(db = Depends(get_db)):
    return PostgresTaskRepository(db)

def get_task_registry(repository = Depends(get_task_repository)):
    return TaskRegistry(repository)

def get_worker_metrics_repository(db = Depends(get_db)):
    return PostgresWorkerMetricsRepository(db)

def get_worker_metrics_registry(repository = Depends(get_worker_metrics_repository)):
    return MetricsRegistry(repository)

def get_dashboard_service(
    worker_repository = Depends(get_worker_repository),
    task_repository = Depends(get_task_repository)
):
    return DashboardService(
        worker_repository,
        task_repository)

def get_training_round_repository(db = Depends(get_db)):
    return TrainingRoundRepository(db)

def get_global_model_repository(db = Depends(get_db)):
    return GlobalModelRepository(db)

def get_global_model_manager(repository = Depends(get_global_model_repository)):
    return GlobalModelManager(repository)

def get_aggregation_strategy():
    return FedAvgStrategy()

def get_aggregation_service(strategy = Depends(get_aggregation_strategy), 
                            global_model_manager = Depends(get_global_model_manager)):
    return AggregationService(strategy, global_model_manager)

def get_round_manager(repository = Depends(get_training_round_repository),
                      task_registry = Depends(get_task_registry), 
                      aggregation_service = Depends(get_aggregation_service)):
    return RoundManager(repository, task_registry, aggregation_service)
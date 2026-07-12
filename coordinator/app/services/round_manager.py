from uuid import uuid4
from datetime import datetime, UTC

from app.db.models.training_round import TrainingRound
from app.models.enums import TaskType, TaskStatus
from app.dto.training_result_dto import TrainingResultDTO


class RoundManager:
    def __init__(self, repository, task_registry, aggregation_service):
        self.repository = repository
        self.task_registry = task_registry
        self.aggregation_service = aggregation_service

    def create_round(
        self, model_name: str, dataset_name: str, num_workers: int,
        epochs: int, batch_size: int, learning_rate: float):
        
        round = TrainingRound(
            round_id=str(uuid4()),
            round_number=1,
            model_name=model_name,
            dataset_name=dataset_name,
            status="RUNNING",
            created_at=datetime.now(UTC),
            completed_at=None
        )

        self.repository.save(round)

        for partition_id in range(num_workers):
            self.task_registry.create_task(
                task_type=TaskType.TRAINING,
                payload={
                    "dataset": dataset_name,
                    "model": model_name,
                    "epochs": epochs,
                    "batch_size": batch_size,
                    "learning_rate": learning_rate,
                    "partition_id": partition_id,
                    "total_partitions": num_workers
                },
                round_id=round.round_id
            )

        return round
    
    def get_round(self, round_id):
        return self.repository.get(round_id)
    
    def get_round_tasks(self,round_id):
        return self.task_registry.repository.get_by_round(round_id)
    
    def get_all_rounds(self):
        return self.repository.get_all()
    
    def is_round_complete(self, round_id):
        tasks = self.get_round_tasks(round_id)
        return all(task.status == TaskStatus.COMPLETED for task in tasks)
    
    def collect_updates(self, round_id):
        tasks = self.get_round_tasks(round_id)
        return [TrainingResultDTO.from_dict(task.result) for task in tasks]
    
    def aggregate_round(self, round_id):
        if not self.is_round_complete(round_id):
            raise ValueError("Round is not complete")

        updates = self.collect_updates(round_id)
        round = self.get_round(round_id)
        aggregated = (
            self.aggregation_service.aggregate(
                round.model_name,
                updates
            )
        )

        round.status = "COMPLETED"
        round.completed_at = datetime.now(UTC)

        self.repository.update(round)

        return aggregated
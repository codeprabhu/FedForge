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
        latest_round = self.repository.get_latest()
        if latest_round is not None and latest_round.status == "RUNNING":
            raise ValueError(
                f"Round {latest_round.round_number} is still running"
            )
        round_number = latest_round.round_number + 1 if latest_round is not None else 1
        round = TrainingRound(
            round_id=str(uuid4()),
            round_number= round_number,
            model_name=model_name,
            dataset_name=dataset_name,
            status="RUNNING",
            created_at=datetime.now(UTC),
            completed_at=None
        )

        self.repository.save(round)

        for partition_id in range(num_workers):
            latest_model = (self.aggregation_service.global_model_manager.get_latest(model_name))
            model_version = (latest_model.version if latest_model is not None else None)

            self.task_registry.create_task(
                task_type=TaskType.TRAINING,
                payload={
                    "dataset": dataset_name,
                    "model": model_name,
                    "model_version": model_version,
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

    def validate_partition_coverage(self, round_id):
        """Validate that a round's completed tasks cover every partition once.

        Partition IDs are the coordinator's durable representation of the
        dataset split.  For a round with ``N`` partitions, the valid set is
        exactly ``0..N-1``.  This catches both duplicate work and gaps before
        model updates are passed to FedAvg.
        """
        tasks = self.get_round_tasks(round_id)
        if not tasks:
            return False, "round has no training tasks"

        partition_counts = {}
        worker_ids = set()
        total_partitions_values = set()
        for task in tasks:
            payload = task.payload or {}
            partition_id = payload.get("partition_id")
            total_partitions = payload.get("total_partitions")
            if not isinstance(partition_id, int) or not isinstance(total_partitions, int):
                return False, f"task {task.task_id} has invalid partition metadata"
            if total_partitions < 1:
                return False, "total_partitions must be positive"

            partition_counts[partition_id] = partition_counts.get(partition_id, 0) + 1
            total_partitions_values.add(total_partitions)
            if task.worker_id is not None:
                worker_ids.add(task.worker_id)

        if len(total_partitions_values) != 1:
            return False, "tasks disagree on total_partitions"
        total_partitions = total_partitions_values.pop()

        if len(tasks) != total_partitions:
            return False, (
                f"expected {total_partitions} tasks, found {len(tasks)}"
            )

        expected = set(range(total_partitions))
        actual = set(partition_counts)
        missing = sorted(expected - actual)
        duplicate = sorted(
            partition_id for partition_id, count in partition_counts.items()
            if count != 1
        )
        unexpected = sorted(actual - expected)
        if missing or duplicate or unexpected:
            return False, (
                f"partition coverage invalid: missing={missing}, "
                f"duplicate={duplicate}, unexpected={unexpected}"
            )

        if len(worker_ids) != total_partitions:
            return False, (
                f"expected {total_partitions} participating workers, "
                f"found {len(worker_ids)}"
            )

        return True, "partition coverage complete"

    def inspect_round(self, round_id):
        """Return completion and coverage state used by the scheduler."""
        tasks = self.get_round_tasks(round_id)
        all_completed = bool(tasks) and all(
            task.status == TaskStatus.COMPLETED for task in tasks
        )
        coverage_valid, coverage_message = self.validate_partition_coverage(round_id)
        return {
            "all_tasks_completed": all_completed,
            "coverage_valid": coverage_valid,
            "coverage_message": coverage_message,
        }
    
    def is_round_complete(self, round_id):
        state = self.inspect_round(round_id)
        return state["all_tasks_completed"] and state["coverage_valid"]

    def is_round_failed(self, round_id):
        return any(task.status == TaskStatus.FAILED for task in self.get_round_tasks(round_id))
    
    def collect_updates(self, round_id):
        tasks = self.get_round_tasks(round_id)
        return [TrainingResultDTO.from_dict(task.result) for task in tasks]
    
    def aggregate_round(self, round_id):
        round = self.get_round(round_id)
        if round is None:
            raise ValueError(f"Round {round_id} does not exist")
        if round.status != "RUNNING":
            raise ValueError(
                f"Cannot aggregate round in status {round.status}"
            )

        state = self.inspect_round(round_id)
        if not state["all_tasks_completed"]:
            raise ValueError("Round is not complete")
        if not state["coverage_valid"]:
            raise ValueError(state["coverage_message"])

        updates = self.collect_updates(round_id)
        print(
    f"[ROUND MANAGER] "
    f"Collected {len(updates)} updates"
)
        if len(updates) == 0:
            print("No updates received")
            return
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

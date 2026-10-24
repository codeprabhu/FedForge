from tasks.echo_task import EchoTask

class TaskExecutor:
    def __init__(self):
        self.echo_task = EchoTask()
        self.training_task = None

    def _get_training_task(self):
        """Load the ML stack only when a training task is actually received."""
        if self.training_task is None:
            from training.registry.dataset_registry import DatasetRegistry
            from training.registry.model_registry import ModelRegistry
            from training.datasets.higgs_dataset import HiggsDataset
            from training.models.higgs_mlp import HiggsMLP
            from training.trainers.local_trainer import LocalTrainer
            from training.tasks.training_task import TrainingTask
            from core.config import COORDINATOR_URL
            from coordinator.worker_client import WorkerClient

            dataset_registry = DatasetRegistry()
            model_registry = ModelRegistry()
            model_registry.register("higgs_mlp", HiggsMLP)
            dataset_registry.register("higgs", HiggsDataset)
            self.training_task = TrainingTask(
                LocalTrainer(), dataset_registry, model_registry,
                WorkerClient(COORDINATOR_URL),
            )
        return self.training_task

    def execute(self, task_type: str, payload: dict):
        if task_type == 'ECHO':
            return self.echo_task.execute(payload)
        
        if task_type == "TRAINING":
            from dto.training_result_dto import TrainingResultsDTO
            from dto.model_weights_dto import ModelWeightsDTO

            result = self._get_training_task().execute(payload)
            return TrainingResultsDTO(
                accuracy=result.accuracy,
                loss=result.loss,
                epochs=result.epochs,
                num_samples=result.num_samples,
                training_time_seconds=result.training_time_seconds,
                model_weights=ModelWeightsDTO(
                    parameters=result.model_weights.weights))
                
        raise ValueError(f"Uknown Task type: {task_type}")

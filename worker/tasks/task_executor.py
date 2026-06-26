from tasks.echo_task import EchoTask

from training.registry.dataset_registry import DatasetRegistry
from training.registry.model_registry import ModelRegistry

from training.datasets.higgs_dataset import HiggsDataset
from training.models.higgs_mlp import HiggsMLP

from training.trainers.local_trainer import LocalTrainer
from training.tasks.training_task import TrainingTask
class TaskExecutor:
    def __init__(self):
        self.echo_task = EchoTask()
        dataset_registry = DatasetRegistry()
        model_registry = ModelRegistry()

        model_registry.register("higgs_mlp", HiggsMLP)
        dataset_registry.register("higgs", HiggsDataset)

        trainer = LocalTrainer()
        self.training_task = TrainingTask(trainer, dataset_registry, model_registry)

    def execute(self, task_type: str, payload: dict):
        if task_type == 'ECHO':
            return self.echo_task.execute(payload)
        
        if task_type == "TRAINING":
            return self.training_task.execute(payload)
                
        raise ValueError(f"Uknown Task type: {task_type}")
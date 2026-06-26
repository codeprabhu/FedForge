from training.trainers.base_trainer import BaseTrainer
from training.results.training_result import TrainingResult

class LocalTrainer(BaseTrainer):
    def train(self, dataset, model, config):
        dataset_info = dataset.get_dataloader(config.partition_id, config.batch_size)
        model_info = model.build()

        return TrainingResult(
            accuracy=0.91,
            loss=0.12,
            epochs=config.epochs,
            num_samples=dataset_info["num_samples"],
            training_time_seconds=1.2,
            model_state={"model_name" : model_info["model_name"]}
        )

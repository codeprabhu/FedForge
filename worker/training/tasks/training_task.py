from training.configs.training_config import TrainingConfig

class TrainingTask:
    def __init__(self, trainer, dataset_registry, model_registry):
        self.trainer= trainer
        self.dataset_registry = dataset_registry
        self.model_registry = model_registry

    def execute(self, payload: dict):
        config = TrainingConfig.from_dict(payload)

        dataset_class = (self.dataset_registry.get(config.dataset))
        model_class = (self.model_registry.get(config.model))

        dataset = dataset_class()
        model = model_class()
        result = self.trainer.train(dataset, model, config)
        return result.to_dict()
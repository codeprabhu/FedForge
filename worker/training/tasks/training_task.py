from training.configs.training_config import TrainingConfig

class TrainingTask:
    def __init__(self, trainer, dataset_registry, model_registry, worker_client):
        self.trainer= trainer
        self.dataset_registry = dataset_registry
        self.model_registry = model_registry
        self.worker_client = worker_client

    def execute(self, payload: dict):
        config = TrainingConfig.from_dict(payload)
        dataset_class = (self.dataset_registry.get(config.dataset))
        model_class = (self.model_registry.get(config.model))
        pretrained_weights = None
        dataset = dataset_class()
        model = model_class()
        if config.model_version is not None:
            global_model = (self.worker_client.get_model(config.model_version))
            pretrained_weights = (global_model["weights"]["parameters"])
        return self.trainer.train(dataset, model, config, pretrained_weights)
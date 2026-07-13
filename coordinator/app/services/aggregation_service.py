class AggregationService:
    def __init__(self, strategy, global_model_manager):
        self.strategy = strategy
        self.global_model_manager = global_model_manager

    def aggregate(self, model_name, results):
        weights = [result.model_weights for result in results]
        aggregated = self.strategy.aggregate(weights)
        model = self.global_model_manager.save_model(model_name,aggregated.to_dict())
        return model
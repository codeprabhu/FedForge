from collections import OrderedDict
import torch # type: ignore
from app.aggregation.strategies.base_aggregation_strategy import BaseAggregationStrategy
from app.dto.model_weights_dto import ModelWeightsDTO

class FedAvgStrategy(BaseAggregationStrategy):
    def aggregate(self, models: list[ModelWeightsDTO], sample_counts: list[int] | None = None)-> ModelWeightsDTO:
        if(len(models) == 0):
            raise ValueError("No Model updates received")
        if sample_counts is None:
            sample_counts = [1] * len(models)
        if len(sample_counts) != len(models) or any(count <= 0 for count in sample_counts):
            raise ValueError("sample_counts must contain one positive count per model")
        total_samples = sum(sample_counts)
        coefficients = [count / total_samples for count in sample_counts]
        state_dicts = [model.to_state_dict() for model in models]
        averaged_state = OrderedDict()

        for key in state_dicts[0]:
            averaged_state[key] = sum(
                (state[key] * coefficient for state, coefficient in zip(state_dicts, coefficients)),
                torch.zeros_like(state_dicts[0][key]),
            )
        return ModelWeightsDTO.from_state_dict(averaged_state)

from collections import OrderedDict
import torch # type: ignore
from base_aggregation_strategy import BaseAggregationStrategy
from dto.model_weights_dto import ModelWeightsDTO

class FedAvgStrategy(BaseAggregationStrategy):
    def aggregate(self, models: list[ModelWeightsDTO])-> ModelWeightsDTO:
        if(len(models) == 0):
            raise ValueError("No Model updates received")
        
        state_dicts = [model.to_state_dict() for model in models]
        averaged_state = OrderedDict()

        for key in state_dicts[0]:
            averaged_state[key] = torch.stack([state[key] for state in state_dicts]).mean(dim = 0)
        return ModelWeightsDTO.from_state_dict(averaged_state)
from abc import ABC, abstractmethod
from app.dto.model_weights_dto import ModelWeightsDTO

class BaseAggregationStrategy(ABC):
    @abstractmethod
    def aggregate(self, models: list[ModelWeightsDTO]) -> ModelWeightsDTO:
        pass
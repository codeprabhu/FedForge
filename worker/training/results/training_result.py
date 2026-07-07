from dataclasses import dataclass
from serialization.model_weights import ModelWeights

@dataclass
class TrainingResult:
    accuracy: float
    loss: float
    epochs: int
    num_samples: int
    training_time_seconds: float
    model_weights: ModelWeights

    def __post_init__(self):
        if self.accuracy < 0:
            raise ValueError()
        if self.loss < 0:
            raise ValueError()
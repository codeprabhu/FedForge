from dataclasses import dataclass
from dto.model_weights_dto import ModelWeightsDTO

@dataclass 
class TrainingResultsDTO:
    accuracy: float
    loss: float
    epochs: int
    num_samples: int
    training_time_seconds: float
    model_weights: ModelWeightsDTO

    def to_dict(self):
        return{
            "accuracy": self.accuracy,
            "loss": self.loss,
            "epochs": self.epochs,
            "num_samples": self.num_samples,
            "training_time_seconds": self.training_time_seconds,
            "model_weights": self.model_weights.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            accuracy = data["accuracy"],
            loss=data["loss"],
            epochs=data["epochs"],
            num_samples=data["num_samples"],

            training_time_seconds=
                data["training_time_seconds"],
            model_weights=
                ModelWeightsDTO.from_dict(data["model_weights"])
        )
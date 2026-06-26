from dataclasses import dataclass

@dataclass
class TrainingResult:
    def __post_init__(self):
        if self.accuracy < 0:
            raise ValueError()
        if self.loss < 0:
            raise ValueError()
        
    accuracy: float
    loss: float

    epochs: int
    num_samples: int

    training_time_seconds: float
    model_state: dict

    def to_dict(self):
        return {
            "accuracy": self.accuracy,
            "loss": self.loss,
            "epochs": self.epochs,
            "num_samples": self.num_samples,
            "training_time_seconds":
                self.training_time_seconds,
            "model_state":
                self.model_state
        }
    
    @classmethod
    def from_dict(cls, payload: dict):
        return cls(
            accuracy=payload["accuracy"],
            loss=payload["loss"],
            epochs=payload["epochs"],
            num_samples=payload["num_samples"],
            training_time_seconds= payload["training_time_seconds"],
            model_state = payload["model_state"]
        )
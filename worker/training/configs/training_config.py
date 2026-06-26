from dataclasses import dataclass

@dataclass
class TrainingConfig:
    dataset: str
    model: str

    epochs: int
    batch_size: int

    learning_rate: float
    partition_id: int

    @classmethod
    def from_dict(cls, payload: dict):
        return cls(
            dataset=payload["dataset"],
            model=payload["model"],
            epochs=payload["epochs"],
            batch_size=payload["batch_size"],
            learning_rate=payload["learning_rate"],
            partition_id=payload["partition_id"]
        )
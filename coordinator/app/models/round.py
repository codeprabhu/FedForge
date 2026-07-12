from pydantic import BaseModel


class CreateRoundRequest(BaseModel):
    model_name: str
    dataset_name: str

    num_workers: int

    epochs: int
    batch_size: int
    learning_rate: float
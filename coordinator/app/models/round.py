from pydantic import BaseModel, Field


class CreateRoundRequest(BaseModel):
    model_name: str
    dataset_name: str

    num_workers: int = Field(gt=0, le=1024)

    epochs: int = Field(gt=0, le=1000)
    batch_size: int = Field(gt=0, le=1_000_000)
    learning_rate: float = Field(gt=0)

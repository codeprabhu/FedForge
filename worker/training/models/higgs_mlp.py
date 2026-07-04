import torch.nn as nn # type: ignore

from training.models.base_model import BaseModel
class HiggsMLP(BaseModel):

    INPUT_FEATURES = 28
    def build(self) -> nn.Module:

        return nn.Sequential(
            nn.Linear(self.INPUT_FEATURES, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1))
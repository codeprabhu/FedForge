from abc import ABC, abstractmethod
import torch.nn as nn # type: ignore
class BaseModel(ABC):
    @abstractmethod
    def build(self) -> nn.Module:
        pass
from __future__ import annotations
from collections import OrderedDict
import torch # type: ignore

class ModelWeights:
    def __init__(self, weights: dict[str, list]):
        self._weights = weights

    @classmethod
    def from_state_dict(cls, state_dict: OrderedDict,)-> "ModelWeights":
        weights = {}
        for name, tensor in state_dict.items():
            weights[name] = tensor.cpu().tolist()

        return cls(weights)
    
    def to_state_dict(self)-> OrderedDict:
        state_dict = OrderedDict()
        for name, values in self._weights.items():
            state_dict[name] = torch.tensor(values)

        return state_dict
    
    def to_dict(self) -> dict:
        return {"weights": self._weights}
    
    @classmethod
    def from_dict(cls, data: dict,) -> "ModelWeights":
        return cls(data["weights"])
    
    @property
    def weights(self):
        return self._weights
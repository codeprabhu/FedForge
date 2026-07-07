from dataclasses import dataclass
from collections import OrderedDict
import torch # type: ignore

@dataclass 
class ModelWeightsDTO:
    parameters : dict

    def to_dict(self):
        return {"parameters": self.parameters}

    @classmethod
    def from_dict(cls, data):
        return cls(parameters=data["parameters"])
    
    def to_state_dict(self):
        state = OrderedDict()
        for name, values in self.parameters.items():
            state[name] = torch.tensor(values)

        return state
    
    @classmethod
    def from_state_dict(cls, state_dict):
        params = {}
        for name, tensor in state_dict.items():
            params[name] = tensor.tolist()
        return cls(params)

    
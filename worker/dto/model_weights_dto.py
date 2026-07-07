from dataclasses import dataclass
@dataclass
class ModelWeightsDTO:
    parameters: dict

    def to_dict(self):
        return {"parameters": self.parameters}
    
    @classmethod
    def from_dict(cls, data):
        return cls(parameters = data["parameters"])
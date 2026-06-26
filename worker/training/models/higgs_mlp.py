from training.models.base_model import BaseModel
class HiggsMLP(BaseModel):
    def build(self):
        return {
            "model_name" : "Higgs_mlp"
        }
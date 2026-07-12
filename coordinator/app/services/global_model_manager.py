from app.repositories.global_model_repository import GlobalModelRepository
from app.db.models.global_model import GlobalModel

class GlobalModelManager:
    def __init__(self, repository):
        self.repository = repository

    def get_latest(self):
        return self.repository.get_latest()
    
    def save_model(self, model_name, weights):
        latest = self.repository.get_latest()
        version = 1
        if latest:
            version = latest.version +1

        model = GlobalModel(
            model_name = model_name,
            version = version, weights = weights)
        
        return self.repository.save(model)
    
    def get_version(self, version: int):
        return self.repository.get_version(version)
    
    
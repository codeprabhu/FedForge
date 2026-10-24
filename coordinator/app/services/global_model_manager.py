from app.repositories.global_model_repository import GlobalModelRepository
from app.db.models.global_model import GlobalModel

class GlobalModelManager:
    def __init__(self, repository):
        self.repository = repository

    def get_latest(self, model_name=None):
        return self.repository.get_latest(model_name)

    def save_model(self, model_name, weights):
        latest = self.repository.get_latest(model_name)
        version = 1
        if latest:
            version = latest.version + 1
        model = GlobalModel(model_name=model_name,
            version=version,weights=weights)
        saved = self.repository.save(model)
        return saved

    def get_version(self, version: int):
        return self.repository.get_version(version)

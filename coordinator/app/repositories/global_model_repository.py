from app.db.models.global_model import GlobalModel
class GlobalModelRepository:
    def __init__(self, db):
        self.db = db

    def save(self, model):
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def get_latest(self, model_name=None):
       query = self.db.query(GlobalModel)
       if model_name is not None:
           query = query.filter(GlobalModel.model_name == model_name)
       return query.order_by(GlobalModel.version.desc()).first()

    def get_version(self, version: int):
        return(self.db.query(GlobalModel).filter(GlobalModel.version == version).first())


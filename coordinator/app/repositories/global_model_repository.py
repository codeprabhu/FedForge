from app.db.models.global_model import GlobalModel
class GlobalModelRepository:
    def __init__(self, db):
        self.db = db

    def save(self, model):
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def get_latest(self):
       return (
                self.db.query(GlobalModel)
                .order_by(GlobalModel.version.desc())
                .first())
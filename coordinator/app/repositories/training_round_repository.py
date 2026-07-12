from app.db.models.task import Task
from app.db.models.training_round import TrainingRound
class TrainingRoundRepository:
    def __init__(self, db):
        self.db = db

    def save(self, round):
        self.db.add(round)
        self.db.commit()
        self.db.refresh(round)
        return round
    
    def get(self, round_id):
        return(self.db.query(TrainingRound).filter(TrainingRound.round_id == round_id).first())
    
    def get_all(self):
        return (self.db.query(TrainingRound).all())

    def delete(self, round_id: str):
        round = self.get(round_id)
        if round is None:
            return

        self.db.delete(round)
        self.db.commit()

    def update(self, round: TrainingRound):
        self.db.commit()
        self.db.refresh(round)

        return round
    
    def get_latest(self):
        return self.db.query(TrainingRound).order_by(TrainingRound.round_number.desc()).first()
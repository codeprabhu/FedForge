from app.db.models.worker_event import WorkerEvent
from app.core.config import EVENT_LIMIT
class WorkerEventRepository:
    def __init__(self, db):
        self.db = db
    
    def save(self, event):
        self.db.add(event)
    
    def get(self, event_id):
        event = self.db.get(WorkerEvent, event_id)
        return event
    
    def get_all(self):
        events = (self.db.query(WorkerEvent)
                .order_by(WorkerEvent.created_at.desc()).all())
        return events

    def get_by_worker(self, worker_id):
        events = (self.db.query(WorkerEvent
                  ).filter(WorkerEvent.worker_id == worker_id
                    ).order_by(WorkerEvent.created_at.desc()          
                        ).all())
        return events
    
    def get_recent(self):
        events = (self.db.query(WorkerEvent
                    ).order_by(WorkerEvent.created_at.desc()
                        ).limit(EVENT_LIMIT).all())
        return events
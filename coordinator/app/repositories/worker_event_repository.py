from coordinator.app.db.models.worker_event import WorkerEvent
from coordinator.app.core.config import EVENT_LIMIT
class WorkerEventRepository:
    def __init__(self, db):
        self.db = db
    
    def _to_dict(self, event):
        return {
            "event_id": event.event_id,
            "worker_id" : event.worker_id,
            "event_type": event.event_type,
            "created_at" : event.created_at
        }
    
    def save(self, event_data):
        event = WorkerEvent(
            worker_id = event_data["worker_id"],
            event_type = event_data["event_type"],
            created_at = event_data["created_at"]
        )

        self.db.add(event)
    
    def get(self, event_id):
        
        event = self.db.get(WorkerEvent, event_id)

        if event is None:
            return None
        return self._to_dict(event)
    
    def get_all(self):
        events = (
            self.db.query(WorkerEvent
                ).order_by(WorkerEvent.created_at.desc())
                    .all()
        )
        return [self._to_dict(event)
                for event in events]

    def get_by_worker(self, worker_id):
        events = (self.db.query(WorkerEvent
                  ).filter(WorkerEvent.worker_id == worker_id
                    ).order_by(WorkerEvent.created_at.desc()          
                        ).all())
        
        return [self._to_dict(event)
                for event in events]
    
    def get_recent(self):
        events = (self.db.query(WorkerEvent
                    ).order_by(WorkerEvent.created_at.desc()
                        ).limit(EVENT_LIMIT).all())
        
        return [self._to_dict(event)
                for event in events]
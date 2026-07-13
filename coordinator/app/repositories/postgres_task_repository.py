from app.db.models.task import Task
from app.repositories.base import Repository
from app.models.enums import TaskStatus
from datetime import datetime,UTC
class PostgresTaskRepository(Repository):

    def __init__(self, db):
        self.db = db

    def save(self, task):
        self.db.add(task)
        self.db.flush()

    def get(self, task_id):

        task = self.db.get(
            Task,
            task_id
        )
        return task

    def get_all(self):

        tasks = (
            self.db.query(Task)
            .order_by(Task.created_at.desc())
            .all()
        )
        return tasks
    
    def get_oldest_created(self):
        task = (self.db.query(Task)
            .filter(Task.status == TaskStatus.CREATED)
            .with_for_update(skip_locked=True)
            .order_by(Task.created_at.asc()).first())
        return task
    
    def update(self, task):
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def get_by_round(self,round_id):
            return (
                self.db.query(Task)
        .       filter(Task.round_id == round_id)
                .all())
    
    def claim_oldest_created(self, worker_id):
        task = (
            self.db.query(Task)
            .filter(Task.status == TaskStatus.CREATED)
            .with_for_update(skip_locked=True)
            .order_by(Task.created_at.asc()).first())

        if task is None:
            return None

        task.status = TaskStatus.ASSIGNED
        task.worker_id = worker_id
        task.assigned_at = datetime.now(UTC)
        self.db.commit()
        self.db.refresh(task)
        return task
from app.db.models.task import Task
from app.repositories.base import Repository


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
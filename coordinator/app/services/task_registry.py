from uuid import uuid4
from datetime import datetime, UTC

from app.db.models.task import Task
from app.models.enums import TaskStatus, TaskType

class TaskRegistry:
    def __init__(self, repository):
        self.repository = repository

    def _get_task_or_raise(self, task_id : str):
        task = self.repository.get(task_id)
        if task is None:
            raise ValueError(f"Task {task_id} DNE")
        return task
    
    def _transition(self, task, expected_status: TaskStatus, new_status: TaskStatus):
        if task.status != expected_status:
            raise ValueError(f"Cannot transition task from {task.status} to {new_status}")
        task.status = new_status

    def create_task(self, task_type:TaskType, payload:dict, round_id: str | None = None):
        task = Task(
            task_id=str(uuid4()),
            round_id = round_id,
            task_type=task_type,
            status=TaskStatus.CREATED,
            worker_id=None,
            payload=payload,
            result=None,
            error_message=None,
            created_at=datetime.now(UTC),
            assigned_at = None,
            started_at=None,
            completed_at=None
        )
        self.repository.save(task)
        return task
    
    def assign_task(self, task_id: str, worker_id: str):
        task= self._get_task_or_raise(task_id)
        self._transition(task, TaskStatus.CREATED, TaskStatus.ASSIGNED)

        task.worker_id = worker_id
        task.assigned_at = datetime.now(UTC)
        self.repository.update(task)
        return task
    
    def start_task(self, task_id:str):
        task = self._get_task_or_raise(task_id)
        self._transition(task, TaskStatus.ASSIGNED, TaskStatus.RUNNING)
        
        task.started_at = datetime.now(UTC)
        self.repository.update(task)
        return task
    
    def complete_task(self, task_id: str, result: dict):
        task = self._get_task_or_raise(task_id)
        self._transition(task, TaskStatus.RUNNING, TaskStatus.COMPLETED)

        task.result = result
        task.completed_at = datetime.now(UTC)
        self.repository.update(task)
        return task
    
    def fail_task(self, task_id: str, error_message: str):
        task = self._get_task_or_raise(task_id)
        if task.status not in (TaskStatus.ASSIGNED, TaskStatus.RUNNING):
            raise ValueError(f"Cannot fail task from state {task.status}")
        
        task.status = TaskStatus.FAILED
        task.error_message = error_message
        task.completed_at = datetime.now(UTC)
        self.repository.update(task)
        return task
    
    def assign_next_task(self, worker_id: str):
        return self.repository.claim_oldest_created(worker_id)

    def requeue_tasks_for_offline_workers(self, workers):
        """Return work owned by offline workers to the shared task queue.

        Training can legitimately take a long time, so elapsed time alone is
        not evidence that a task failed. A task is recoverable only when its
        assigned worker is known to be offline.
        """
        online_worker_ids = {
            worker.worker_id for worker in workers
            if getattr(worker.status, "value", worker.status) == "ONLINE"
        }
        requeued_tasks = []
        for task in self.repository.get_all():
            if task.status not in (TaskStatus.ASSIGNED, TaskStatus.RUNNING):
                continue
            if task.worker_id is not None and task.worker_id not in online_worker_ids:
                task.status = TaskStatus.CREATED
                task.worker_id = None
                task.assigned_at = None
                task.started_at = None
                task.error_message = None
                self.repository.update(task)
                requeued_tasks.append(task)
        return requeued_tasks

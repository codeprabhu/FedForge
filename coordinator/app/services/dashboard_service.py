from app.models.enums import TaskStatus

class DashboardService:
    def __init__(self, worker_repository, task_repository):
        self.worker_repository = worker_repository
        self.task_repository = task_repository

    def get_dashboard(self):
        workers = self.worker_repository.get_all()
        tasks = self.task_repository.get_all()

        workers_online = len(workers)

        running_tasks = len([
            task for task in tasks
            if task.status == TaskStatus.RUNNING
        ])

        completed_tasks = len([
            task for task in tasks
            if task.status == TaskStatus.COMPLETED
        ])

        return {
            "workers_online": workers_online,
            "running_tasks": running_tasks,
            "completed_tasks": completed_tasks,
            "coordinator_status": "ONLINE"
        }
from tasks.echo_task import EchoTask

class TaskExecutor:
    def __init__(self):
        self.echo_task = EchoTask()

    def execute(self, task_type: str, payload: dict):
        if task_type == 'ECHO':
            return self.echo_task.execute(payload)
        
        raise ValueError(f"Uknown Task type: {task_type}")
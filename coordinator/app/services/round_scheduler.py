import asyncio
from app.db.unit_of_work import UnitOfWork

from app.repositories.postgres_worker_repository import PostgresWorkerRepository
from app.repositories.training_round_repository import TrainingRoundRepository
from app.repositories.postgres_task_repository import PostgresTaskRepository
from app.repositories.global_model_repository import GlobalModelRepository

from app.services.task_registry import TaskRegistry
from app.services.round_manager import RoundManager
from app.services.global_model_manager import GlobalModelManager
from app.services.aggregation_service import AggregationService
from app.aggregation.strategies.fedavg_strategy import FedAvgStrategy

class RoundScheduler:

    def __init__(self):
        self.running = True

    def stop(self):
        self.running = False

    async def scheduler_loop(self):

        while self.running:
            try:
                with UnitOfWork() as db:
                    worker_repository = (PostgresWorkerRepository(db))
                    round_repository = (TrainingRoundRepository(db))
                    task_repository = (PostgresTaskRepository(db))
                    global_model_repository = (GlobalModelRepository(db))
                    task_registry = (TaskRegistry(task_repository))
                    global_model_manager = (GlobalModelManager(global_model_repository))

                    aggregation_service = (AggregationService(
                            FedAvgStrategy(),global_model_manager))

                    round_manager = (RoundManager(round_repository,
                            task_registry,aggregation_service))

                    requeued_tasks = task_registry.requeue_tasks_for_offline_workers(
                        worker_repository.get_all()
                    )
                    if requeued_tasks:
                        print(
                            f"[ROUND SCHEDULER] Requeued {len(requeued_tasks)} task(s)"
                        )
                    await self.tick(round_manager, worker_repository)

            except Exception as e:
                print(f"[ROUND SCHEDULER] {e}")

            await asyncio.sleep(5)

    async def tick(self,round_manager,worker_repository):
        rounds = (round_manager.get_all_rounds())
        active_round = next((r for r in rounds
                if r.status == "RUNNING"),None)

        if active_round is None:
            latest_round = round_manager.repository.get_latest()
            if latest_round is not None and latest_round.status == "FAILED":
                print(
                    f"[ROUND SCHEDULER] Waiting after failed round "
                    f"{latest_round.round_number}"
                )
                return
            workers = [worker for worker in worker_repository.get_all()
                if worker.status == "ONLINE"]
            if len(workers) == 0:
                return
            print("[ROUND SCHEDULER] Creating round")

            round_manager.create_round(
                model_name="higgs_mlp",
                dataset_name="higgs",
                num_workers=len(workers),
                epochs=5,
                batch_size=128,
                learning_rate=0.001
            )
            return

        state = round_manager.inspect_round(active_round.round_id)
        if state["all_tasks_completed"] and not state["coverage_valid"]:
            print(
                f"[ROUND SCHEDULER] Failing round "
                f"{active_round.round_number}: {state['coverage_message']}"
            )
            active_round.status = "FAILED"
            round_manager.repository.update(active_round)
        elif round_manager.is_round_complete(active_round.round_id):
            print(f"[ROUND SCHEDULER] "
                f"Aggregating round "f"{active_round.round_number}")
            round_manager.aggregate_round(active_round.round_id)
        elif round_manager.is_round_failed(active_round.round_id):
            active_round.status = "FAILED"
            round_manager.repository.update(active_round)


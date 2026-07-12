from fastapi import APIRouter, Depends # type: ignore
from app.api.dependencies import get_round_manager
from app.services.round_manager import RoundManager
from app.models.round import CreateRoundRequest

router = APIRouter()

@router.post("/rounds")
def create_round(
    payload: CreateRoundRequest,
    manager: RoundManager =
        Depends(get_round_manager)
):
    return manager.create_round(
        model_name=payload.model_name,
        dataset_name=payload.dataset_name,
        num_workers=payload.num_workers,
        epochs=payload.epochs,
        batch_size=payload.batch_size,
        learning_rate=payload.learning_rate)

@router.post("/rounds/{round_id}/aggregate")
def aggregate_round(round_id: str,
    manager: RoundManager =
        Depends(get_round_manager)):
    manager.aggregate_round(round_id)
    return {"status": "aggregation completed"}

@router.get("/rounds")
def get_rounds(
    manager: RoundManager =
        Depends(get_round_manager)
):
    return manager.repository.get_all_rounds()

@router.get("/rounds/{round_id}")
def get_round(
    round_id: str,
    manager: RoundManager =
        Depends(get_round_manager)
):
    return manager.get_round(round_id)
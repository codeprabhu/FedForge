from fastapi import APIRouter, Depends, Query # type: ignore
from app.api.dependencies import get_global_model_manager

router = APIRouter()

@router.get("/global-model/latest")
def latest_model(
    include_weights: bool = Query(default=True),
    manager = Depends(get_global_model_manager),
):
    model = manager.get_latest()
    if model is None or include_weights:
        return model
    return {
        "model_id": model.model_id,
        "model_name": model.model_name,
        "version": model.version,
        "created_at": model.created_at,
    }

@router.get("/global-model/{version}")
def get_model(version : int, manager = Depends(get_global_model_manager)):
    return manager.get_version(version)

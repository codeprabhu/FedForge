from fastapi import APIRouter, Depends # type: ignore
from app.api.dependencies import get_global_model_manager

router = APIRouter()

@router.get("/global-model/latest")
def latest_model(manager = Depends(get_global_model_manager)):
    return manager.get_latest()

@router.get("/global-model/{version}")
def get_model(version : int, manager = Depends(get_global_model_manager)):
    return manager.get_version(version)
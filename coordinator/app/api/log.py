from fastapi import APIRouter, Depends # type: ignore

from app.api.dependencies import get_worker_event_repository

router = APIRouter()

@router.get("/logs")
def get_logs(
    repository = Depends(get_worker_event_repository)
):
    events = repository.get_all()

    events = sorted(
        events,
        key=lambda x: x.created_at,
        reverse=True
    )

    return events[:20]
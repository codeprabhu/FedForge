from fastapi import APIRouter, Depends # type: ignore

from app.api.dependencies import get_dashboard_service
from app.services.dashboard_service import DashboardService

router = APIRouter()

@router.get("/dashboard")
def get_dashboard(
    dashboard_service: DashboardService =
        Depends(get_dashboard_service)
):
    return dashboard_service.get_dashboard()
from fastapi import APIRouter, Depends

from backend.services.launch_service import SpaceXService
from backend.models.models import LaunchFilterRequest, StatisticsResponse, LaunchListResponse

router = APIRouter()
service = SpaceXService()

@router.get("/launches", response_model=LaunchListResponse)
async def get_launches(filters: LaunchFilterRequest = Depends()):
    launches = await service.filter_launches(**filters.dict(exclude_none=True))
    return LaunchListResponse(launches=launches)

@router.get("/statistics", response_model=StatisticsResponse)
async def get_stats():
    success_rate = await service.get_success_rate_by_rocket()
    launch_count = await service.get_launch_count_by_launchpad()
    launch_freq = await service.get_launch_frequency()

    response = StatisticsResponse(
        success_rate_by_rocket=success_rate,
        launch_count_by_launchpad=launch_count,
        launch_frequency=launch_freq,
    )
    return response

from fastapi import APIRouter

from src.api.services.health_service import HealthService

router = APIRouter()
health_service = HealthService()


@router.get("/ready", status_code=200, tags=["health"])
async def ready():
    return health_service.ready()


@router.get("/live", status_code=200, tags=["health"])
async def live():
    return health_service.live()

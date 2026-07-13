"""
Health probe — used by Docker / k8s / load balancers.
"""
from datetime import datetime, timezone

from fastapi import APIRouter

from ..config import get_settings
from ..schemas import HealthOut

router = APIRouter(tags=["meta"])


@router.get("/api/health", response_model=HealthOut)
async def health() -> HealthOut:
    settings = get_settings()
    return HealthOut(status="ok", version=settings.api_version,
                     time=datetime.now(timezone.utc))

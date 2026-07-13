"""
Public services catalog endpoint.
"""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.service import Service
from ..schemas import ServiceOut

router = APIRouter(prefix="/api/services", tags=["catalog"])


@router.get("", response_model=list[ServiceOut])
async def list_services(db: AsyncSession = Depends(get_db)) -> list[ServiceOut]:
    stmt = select(Service).where(Service.is_active.is_(True)).order_by(Service.order)
    rows = (await db.execute(stmt)).scalars().all()
    return [
        ServiceOut(
            id=s.id,
            slug=s.slug,
            title=s.title,
            description=s.description,
            features=s.feature_list(),
            price_from=s.price_from,
            currency=s.currency,
            badge=s.badge,
        )
        for s in rows
    ]

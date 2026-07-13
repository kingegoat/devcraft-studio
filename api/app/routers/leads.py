"""
Lead endpoints — public POST + admin-only GET/PATCH.
"""
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import get_settings
from ..database import get_db
from ..schemas import LeadCreate, LeadOut, LeadStatusUpdate
from ..services.leads import LeadsService

router = APIRouter(prefix="/api", tags=["leads"])
_settings = get_settings()


async def _require_admin(authorization: Optional[str] = Header(None)) -> None:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing bearer token")
    token = authorization.split(" ", 1)[1].strip()
    if token != _settings.admin_token:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid token")


@router.post("/lead", response_model=LeadOut, status_code=status.HTTP_201_CREATED)
async def create_lead(
    payload: LeadCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> LeadOut:
    """Submit a new lead from the marketing site."""
    ip = request.client.host if request.client else None
    ua = request.headers.get("user-agent")

    svc = LeadsService(db)
    lead = await svc.create(payload, ip=ip, user_agent=ua)
    return LeadOut.model_validate(lead)


@router.get("/leads", response_model=list[LeadOut], dependencies=[Depends(_require_admin)])
async def list_leads(
    status_filter: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
) -> list[LeadOut]:
    """Admin: list leads (filter by status)."""
    leads = await LeadsService(db).list(status=status_filter, limit=limit, offset=offset)
    return [LeadOut.model_validate(l) for l in leads]


@router.patch("/leads/{lead_id}", response_model=LeadOut,
              dependencies=[Depends(_require_admin)])
async def update_lead_status(
    lead_id: int,
    payload: LeadStatusUpdate,
    db: AsyncSession = Depends(get_db),
) -> LeadOut:
    lead = await LeadsService(db).update_status(lead_id, payload)
    if not lead:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Lead not found")
    return LeadOut.model_validate(lead)

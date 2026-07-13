"""
Lead-related business logic: creation, listing, status updates, bot forwarding.
"""
from typing import List, Optional, Sequence

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import get_settings
from ..models.lead import Lead
from ..schemas import LeadCreate, LeadStatusUpdate

_settings = get_settings()


class LeadsService:
    """Encapsulates lead CRUD and side-effects (bot notification)."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, data: LeadCreate, *, ip: Optional[str] = None,
                     user_agent: Optional[str] = None) -> Lead:
        """Persist a new lead and trigger best-effort bot notification."""
        lead = Lead(
            name=data.name,
            email=str(data.email),
            service=data.service,
            message=data.message,
            source=data.source or "site",
            lang=data.lang or "ru",
            ip=ip,
            user_agent=user_agent,
        )
        self.db.add(lead)
        await self.db.flush()  # populate lead.id
        await self.db.refresh(lead)

        # Best-effort fan-out to Telegram bot
        if _settings.bot_notify_url:
            await self._notify_bot(lead)

        return lead

    async def list(self, *, status: Optional[str] = None, limit: int = 100,
                   offset: int = 0) -> Sequence[Lead]:
        stmt = select(Lead).order_by(Lead.created_at.desc()).limit(limit).offset(offset)
        if status:
            stmt = stmt.where(Lead.status == status)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get(self, lead_id: int) -> Optional[Lead]:
        return await self.db.get(Lead, lead_id)

    async def update_status(self, lead_id: int, payload: LeadStatusUpdate) -> Optional[Lead]:
        lead = await self.db.get(Lead, lead_id)
        if not lead:
            return None
        lead.status = payload.status
        if payload.notes is not None:
            lead.notes = payload.notes
        await self.db.flush()
        await self.db.refresh(lead)
        return lead

    async def _notify_bot(self, lead: Lead) -> None:
        """Forward the lead to the bot's webhook so admins get a Telegram alert."""
        try:
            payload = {
                "type": "new_lead",
                "lead": {
                    "id": lead.id,
                    "name": lead.name,
                    "email": lead.email,
                    "service": lead.service,
                    "message": lead.message,
                    "lang": lead.lang,
                },
            }
            async with httpx.AsyncClient(timeout=_settings.bot_notify_timeout) as client:
                await client.post(_settings.bot_notify_url, json=payload)
        except Exception as exc:  # noqa: BLE001 — never let bot failure break lead capture
            # In production: emit a metric/log for monitoring.
            print(f"[leads] bot notification failed: {exc!r}")

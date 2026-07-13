"""HTTP client wrapping the FastAPI backend."""
from __future__ import annotations

from typing import Any

import httpx

from .config import get_settings


class APIClient:
    """Thin wrapper around the project's REST API."""

    def __init__(self) -> None:
        s = get_settings()
        self._base = s.api_base_url.rstrip("/")
        self._token = s.api_admin_token
        self._client = httpx.AsyncClient(
            base_url=self._base,
            timeout=10.0,
            headers={"Authorization": f"Bearer {self._token}"} if self._token else {},
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def ping(self) -> bool:
        try:
            r = await self._client.get("/api/health")
            return r.status_code == 200
        except httpx.HTTPError:
            return False

    async def get_services(self) -> list[dict[str, Any]]:
        r = await self._client.get("/api/services")
        r.raise_for_status()
        return r.json()

    async def get_projects(self) -> list[dict[str, Any]]:
        r = await self._client.get("/api/projects")
        r.raise_for_status()
        return r.json()

    async def create_lead(self, payload: dict[str, Any]) -> dict[str, Any]:
        r = await self._client.post("/api/lead", json=payload)
        r.raise_for_status()
        return r.json()

    async def notify_new_lead(self, payload: dict[str, Any]) -> dict[str, Any]:
        """If API exposed an internal notify endpoint, forward lead to admin chat.

        Falls back to direct admin notification in handlers/lead.py if absent.
        """
        r = await self._client.post("/api/internal/notify-lead", json=payload)
        r.raise_for_status()
        return r.json()


api = APIClient()

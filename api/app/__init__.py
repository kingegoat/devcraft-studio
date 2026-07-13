"""
DevCraft Studio — FastAPI backend
REST API for the marketing site and Telegram bot.

Endpoints
---------
POST   /api/lead              Submit a contact form lead
GET    /api/leads             List leads (admin, token-protected)
GET    /api/services          Public services catalog
GET    /api/projects          Public projects/portfolio list
GET    /api/health            Liveness probe
GET    /                      Service banner

Run
---
    uvicorn app.main:app --reload --port 8000

Environment
-----------
    API_HOST, API_PORT, API_DEBUG
    DATABASE_URL             e.g. sqlite:///./dev.db  or  postgresql+asyncpg://...
    BOT_NOTIFY_URL           Optional: URL to forward new leads to (e.g. Telegram bot webhook)
    ADMIN_TOKEN              Bearer token to authorize /api/leads
"""

from .main import app

__all__ = ["app"]

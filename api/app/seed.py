"""
Seed initial catalog data (services + projects) so the API is useful out of the box.
Idempotent: only inserts rows that don't already exist.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models.project import Project
from .models.service import Service


SERVICES = [
    {
        "slug": "landing",
        "title": "Landing pages & business cards",
        "description": "Responsive layout, clean code, instant load. Mobile-first, cross-browser, SEO-ready.",
        "features": "Mobile-first responsive,Animations & interactivity,SEO and OpenGraph",
        "price_from": 30000,
        "currency": "USD",
        "badge": None,
        "order": 1,
    },
    {
        "slug": "telegram-bot",
        "title": "Telegram bots",
        "description": "From a simple FAQ bot to complex systems with payments, CRM integration and admin panel.",
        "features": "aiogram 3, webhooks,Telegram Stars payments,Inline mode and FSM",
        "price_from": 50000,
        "currency": "USD",
        "badge": "Popular",
        "order": 2,
    },
    {
        "slug": "api",
        "title": "Web services & APIs",
        "description": "FastAPI/Django backend with REST, auth, PostgreSQL and Docker deployment.",
        "features": "REST + WebSocket,JWT, OAuth2,CI/CD and monitoring",
        "price_from": 70000,
        "currency": "USD",
        "badge": None,
        "order": 3,
    },
]


PROJECTS = [
    {
        "slug": "fintess",
        "title": "Fintess — fitness coach",
        "description": "Responsive landing with class booking and Telegram integration.",
        "tag": "Landing",
        "stack": "HTML,CSS,JavaScript,aiogram",
        "repo_url": "https://github.com/devcraft/fintess",
        "demo_url": "https://fintess.devcraft.studio",
        "cover_color": "#f97316",
        "order": 1,
    },
    {
        "slug": "leadflow",
        "title": "LeadFlow — leads CRM",
        "description": "FastAPI + PostgreSQL web service with Telegram notifications.",
        "tag": "SaaS",
        "stack": "Python,FastAPI,PostgreSQL,Docker",
        "repo_url": "https://github.com/devcraft/leadflow",
        "demo_url": None,
        "cover_color": "#06b6d4",
        "order": 2,
    },
    {
        "slug": "orderbot",
        "title": "OrderBot — order intake",
        "description": "aiogram 3 Telegram bot with FSM, payments and admin panel.",
        "tag": "Bot",
        "stack": "Python,aiogram,SQLite,Docker",
        "repo_url": "https://github.com/devcraft/orderbot",
        "demo_url": None,
        "cover_color": "#8b5cf6",
        "order": 3,
    },
    {
        "slug": "polyglot-ui",
        "title": "Polyglot UI",
        "description": "UI kit with RU/EN/DE/ES/FR switching without page reload.",
        "tag": "Multilang",
        "stack": "HTML,CSS,JavaScript,i18n",
        "repo_url": "https://github.com/devcraft/polyglot-ui",
        "demo_url": "https://polyglot.devcraft.studio",
        "cover_color": "#10b981",
        "order": 4,
    },
]


async def seed_catalog(db: AsyncSession) -> None:
    for s in SERVICES:
        exists = await db.execute(select(Service).where(Service.slug == s["slug"]))
        if exists.scalar_one_or_none():
            continue
        db.add(Service(**s))

    for p in PROJECTS:
        exists = await db.execute(select(Project).where(Project.slug == p["slug"]))
        if exists.scalar_one_or_none():
            continue
        db.add(Project(**p))

    await db.commit()

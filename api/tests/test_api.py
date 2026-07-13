"""Smoke tests for the API."""
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import create_app


@pytest.fixture
async def client():
    app = create_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        # trigger lifespan
        async with app.router.lifespan_context(app):
            yield c


@pytest.mark.asyncio
async def test_health(client):
    r = await client.get("/api/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "version" in body


@pytest.mark.asyncio
async def test_create_lead(client):
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "service": "landing",
        "message": "Hello, I'd like to discuss a project please.",
        "lang": "en",
    }
    r = await client.post("/api/lead", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["email"] == "test@example.com"
    assert body["status"] == "new"


@pytest.mark.asyncio
async def test_invalid_email(client):
    payload = {
        "name": "Test",
        "email": "not-an-email",
        "service": "landing",
        "message": "Hello there, this is a valid message.",
    }
    r = await client.post("/api/lead", json=payload)
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_short_message(client):
    payload = {
        "name": "Test",
        "email": "test@example.com",
        "service": "landing",
        "message": "hi",
    }
    r = await client.post("/api/lead", json=payload)
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_admin_requires_auth(client):
    r = await client.get("/api/leads")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_admin_lists_leads(client):
    await client.post("/api/lead", json={
        "name": "Alice", "email": "alice@example.com",
        "service": "bot", "message": "Need a Telegram bot.",
    })
    r = await client.get("/api/leads", headers={"Authorization": "Bearer test-admin"})
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) >= 1


@pytest.mark.asyncio
async def test_services_seeded(client):
    r = await client.get("/api/services")
    assert r.status_code == 200
    slugs = {s["slug"] for s in r.json()}
    assert {"landing", "telegram-bot", "api"}.issubset(slugs)


@pytest.mark.asyncio
async def test_projects_seeded(client):
    r = await client.get("/api/projects")
    assert r.status_code == 200
    assert len(r.json()) >= 4

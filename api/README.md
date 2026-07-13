# DevCraft Studio API

Async REST API for the marketing site and Telegram bot, built on FastAPI + SQLAlchemy 2.0 (async).

## Endpoints

| Method | Path                       | Auth   | Description                          |
| ------ | -------------------------- | ------ | ------------------------------------ |
| POST   | `/api/lead`                | none   | Submit contact-form lead             |
| GET    | `/api/leads`               | admin  | List leads (filter by status)        |
| PATCH  | `/api/leads/{id}`          | admin  | Update lead status / notes           |
| GET    | `/api/services`            | none   | Public services catalog              |
| GET    | `/api/projects`            | none   | Public portfolio list                |
| GET    | `/api/health`              | none   | Liveness probe                       |
| GET    | `/api/docs`                | none   | Swagger UI                           |
| GET    | `/api/redoc`               | none   | ReDoc UI                             |

`/api/leads` and `/api/leads/{id}` require `Authorization: Bearer <ADMIN_TOKEN>`.

## Run locally

```bash
cd api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # edit if needed
uvicorn app.main:app --reload --port 8000
```

Open <http://localhost:8000/api/docs>.

The first start creates `dev.db` (SQLite) and seeds catalog rows.

## Architecture

```
app/
├── main.py            # FastAPI factory + lifespan
├── config.py          # pydantic-settings env loader
├── database.py        # async SQLAlchemy engine/session
├── seed.py            # idempotent catalog seed
├── schemas.py         # Pydantic v2 request/response models
├── models/            # SQLAlchemy ORM
│   ├── lead.py
│   ├── project.py
│   └── service.py
├── routers/           # HTTP controllers
│   ├── health.py
│   ├── leads.py
│   ├── projects.py
│   └── services.py
└── services/          # business logic
    └── leads.py
```

## Switching to PostgreSQL

Set `DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/devcraft` and re-run. No code changes needed.

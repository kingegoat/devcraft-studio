# DevCraft Studio · monorepo

Production-ready full-stack reference project: **marketing landing page + FastAPI backend + Telegram bot**, all sharing one database and one deployment story.

Built to demonstrate the same stack I ship for clients:

| Layer    | Stack                                                                                |
| -------- | ------------------------------------------------------------------------------------ |
| Frontend | Vanilla **HTML5 / CSS3 / ES2024** — no framework, mobile-first, dark/light, i18n     |
| Backend  | **FastAPI 0.115** · SQLAlchemy 2.0 async · Pydantic v2 · SQLite or PostgreSQL        |
| Bot      | **aiogram 3** · FSM · multi-language · admin notifications via webhook               |
| DevOps   | Docker · docker-compose · Nginx · GitHub Actions–ready                                |

The whole stack runs locally in <2 minutes and ships to production in a single `docker compose up`.

```
                    ┌─────────────────────────────────┐
                    │   Marketing site (static SPA)   │
                    │   /site  →  HTML + CSS + JS     │
                    └────────────┬────────────────────┘
                                 │ fetch /api/lead, /api/services
                                 ▼
   ┌─────────────────────────────────────────────────────────┐
   │              FastAPI   :8000                              │
   │   /api/lead    /api/leads    /api/services    /api/docs  │
   └─────┬───────────────────────────────────────┬─────────────┘
         │ async SQLAlchemy                      │ HTTP notify
         ▼                                       ▼
   ┌─────────────┐                       ┌─────────────────┐
   │ PostgreSQL  │                       │ Telegram bot    │
   │  (or SQLite)│                       │ aiogram 3 · :8080│
   └─────────────┘                       └────────┬────────┘
                                                   │ Bot API
                                                   ▼
                                          ┌──────────────────┐
                                          │  Telegram users  │
                                          └──────────────────┘
```

## Layout

```
devcraft-studio/
├── site/             # marketing landing page (static)
│   ├── index.html
│   ├── css/style.css
│   ├── js/app.js
│   ├── i18n/{ru,en,de}.json
│   └── assets/
├── api/              # FastAPI backend
│   ├── app/
│   │   ├── main.py            # factory + lifespan
│   │   ├── config.py          # pydantic-settings
│   │   ├── database.py        # async SQLAlchemy
│   │   ├── seed.py
│   │   ├── schemas.py
│   │   ├── models/{lead,project,service}.py
│   │   ├── routers/{health,leads,services,projects}.py
│   │   └── services/leads.py
│   ├── tests/                # 8 unit tests, pytest-asyncio
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── bot/              # Telegram bot (aiogram 3)
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── api_client.py
│   │   ├── i18n.py
│   │   ├── store.py
│   │   ├── locales/{ru,en,de}.json
│   │   ├── handlers/{common,services,portfolio,about,contact,language}.py
│   │   ├── keyboards/builtin.py
│   │   └── middlewares/user_context.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── infra/
│   ├── docker-compose.yml    # api + bot + postgres + nginx
│   ├── nginx.conf
│   ├── deploy.sh
│   └── .env.example
├── docs/
└── README.md
```

## Quick start (local, all three services)

```bash
# 1. clone & enter
git clone https://github.com/devcraft/devcraft-studio.git
cd devcraft-studio

# 2. backend
cd api && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env  # edit if needed
pytest -v             # 8 tests, should all pass
uvicorn app.main:app --reload --port 8000
# open http://localhost:8000/api/docs

# 3. bot (separate terminal)
cd ../bot && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # set BOT_TOKEN, ADMIN_CHAT_IDS, API_BASE_URL
python -m app.main

# 4. site — open site/index.html in your browser, or:
cd ../site && python3 -m http.server 5173
```

## Production (one command)

```bash
cd infra
cp .env.example .env  # set BOT_TOKEN, ADMIN_TOKEN, ADMIN_CHAT_IDS, DATABASE_URL
./deploy.sh
```

This brings up **Nginx → FastAPI → Telegram bot → PostgreSQL** as four containers behind a single network.

## Endpoints

| Method | Path                       | Description                          |
| ------ | -------------------------- | ------------------------------------ |
| POST   | `/api/lead`                | Submit contact-form lead             |
| GET    | `/api/leads`               | List leads (admin token)             |
| PATCH  | `/api/leads/{id}`          | Update lead status / notes           |
| GET    | `/api/services`            | Public services catalog              |
| GET    | `/api/projects`            | Public portfolio list                |
| GET    | `/api/health`              | Liveness probe                       |
| GET    | `/api/docs`                | Swagger UI                           |
| POST   | `/bot/webhook`             | Telegram webhook receiver            |

## What this project demonstrates

- **Frontend craftsmanship** — semantic HTML, mobile-first CSS with custom properties, no framework bloat, i18n via JSON dict + fetch, dark/light theme toggle, intersection-observer reveals, accessible (skip-link, ARIA, reduced-motion).
- **Backend engineering** — async SQLAlchemy 2.0, Pydantic v2 validation, service-layer separation, idempotent seeding, admin auth via bearer token, OpenAPI docs for free, structured error handling.
- **Bot UX** — aiogram 3 with FSM (multi-step lead intake), inline keyboards, per-user language persistence, admin notifications, polling + webhook modes.
- **DevOps** — dockerized, docker-compose orchestration, healthchecks, Nginx reverse proxy with single-port deployment, env-var configuration.

## Testing

```bash
cd api
pytest -v
# 8 passed in ~0.5s
```

## Tech choices & rationale

- **Vanilla frontend** instead of React/Next: matches my "clean code, fast load" positioning for Kwork landing gigs. The site is fast because there's nothing to load.
- **SQLite default** for development; **PostgreSQL** in production via env var. No code changes.
- **aiogram 3 over python-telegram-bot**: aiogram has native async + FSM + webhook support, which is exactly the same stack as the FastAPI backend.
- **Single-port deployment** via Nginx: the static site, API and bot webhook all share one HTTPS port.

## License

MIT — use as a reference, fork, learn. Attribution appreciated but not required.

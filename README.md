# DevCraft Studio · monorepo

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](api/requirements.txt)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](api/)
[![aiogram 3](https://img.shields.io/badge/aiogram-3.x-blue.svg)](bot/)
[![Tests](https://img.shields.io/badge/tests-8%20passed-brightgreen.svg)](api/tests/)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

</div>

Full-stack reference project: **marketing landing page + FastAPI backend + Telegram bot**, sharing one database and one deployment story.

| Layer    | Stack                                                                                |
| -------- | ------------------------------------------------------------------------------------ |
| Frontend | Vanilla **HTML5 / CSS3 / ES2024** — no framework, mobile-first, dark/light, i18n     |
| Backend  | **FastAPI 0.115** · SQLAlchemy 2.0 async · Pydantic v2 · SQLite or PostgreSQL        |
| Bot      | **aiogram 3** · FSM · admin notifications · polling + webhook                       |
| DevOps   | Docker · docker-compose · Nginx                                                      |

The whole stack runs locally in <2 minutes and ships to production in a single `docker compose up`.

```
                    ┌─────────────────────────────────┐
                    │   Marketing site (static)       │
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
├── site/             # marketing landing page (vanilla HTML/CSS/JS)
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
│   │   ├── models/{lead,service}.py
│   │   ├── routers/{health,leads,services}.py
│   │   └── services/leads.py
│   ├── tests/                # 8 unit tests, pytest-asyncio
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── bot/              # Telegram bot (aiogram 3)
│   ├── app/
│   │   ├── main.py            # entry, dispatcher wiring
│   │   ├── config.py
│   │   ├── api_client.py
│   │   ├── states.py
│   │   ├── handlers/{common,contact}.py
│   │   ├── keyboards/builtin.py
│   │   └── locales/ru.json
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── infra/
│   ├── docker-compose.yml    # api + bot + postgres + nginx
│   ├── nginx.conf
│   ├── deploy.sh
│   └── .env.example
└── README.md
```

## Quick start (local)

```bash
# backend
cd api
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
pytest -v             # 8 tests
uvicorn app.main:app --reload --port 8000
# open http://localhost:8000  (site + Swagger at /api/docs)

# bot (separate terminal)
cd ../bot
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # set BOT_TOKEN, ADMIN_CHAT_IDS
python -m app.main
```

## Production

```bash
cd infra
cp .env.example .env  # BOT_TOKEN, ADMIN_TOKEN, ADMIN_CHAT_IDS, DATABASE_URL
./deploy.sh
```

Brings up Nginx → FastAPI → Telegram bot → PostgreSQL as four containers behind one network.

## Endpoints

| Method | Path            | Auth  | Description                          |
| ------ | --------------- | ----- | ------------------------------------ |
| POST   | `/api/lead`     | none  | Submit contact-form lead             |
| GET    | `/api/leads`    | admin | List leads                           |
| PATCH  | `/api/leads/{id}` | admin | Update lead status / notes         |
| GET    | `/api/services` | none  | Public services catalog              |
| GET    | `/api/health`   | none  | Liveness probe                       |
| GET    | `/api/docs`     | none  | Swagger UI                           |
| POST   | `/bot/webhook`  | none  | Telegram webhook receiver            |

## Bot commands

| Command     | What it does                  |
| ----------- | ----------------------------- |
| `/start`    | One-screen service picker     |
| `/contacts` | Show contact channels         |
| `/cancel`   | Exit current step (FSM escape)|
| `/help`     | List commands                 |

## Testing

```bash
cd api
pytest -v
# 8 passed in ~0.5s
```

## License

MIT — fork, learn, ship. Attribution appreciated but not required.

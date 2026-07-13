# DevCraft Studio — Telegram Bot

Multi-language Telegram bot (RU/EN/DE) built on **aiogram 3** + FastAPI backend integration.
Supports services catalog, portfolio, lead intake (FSM), and admin notifications.

## Features

- 🌍 i18n: switch between RU / EN / DE per user
- 🛠 Services catalog with inline detail and one-tap "order"
- 💼 Portfolio fetched live from the API
- ✉️ Lead intake via FSM (name → email → message) → persisted through `/api/lead`
- 🔔 Admin notifications in Telegram (polled or via internal webhook)
- 💾 Tiny JSON user store for language/FSM persistence (swap for Redis in prod)

## Project layout

```
bot/
├── app/
│   ├── main.py            # entry point, dispatcher wiring
│   ├── config.py          # pydantic-settings
│   ├── api_client.py      # async client for the FastAPI backend
│   ├── i18n.py            # dictionary loader
│   ├── store.py           # user persistence
│   ├── locales/           # ru.json, en.json, de.json
│   ├── handlers/          # aiogram routers
│   │   ├── common.py      # /start, menu, language switch
│   │   ├── language.py    # change language
│   │   ├── services.py    # services catalog
│   │   ├── portfolio.py   # portfolio feed
│   │   ├── about.py       # static info
│   │   └── contact.py     # lead intake FSM
│   ├── keyboards/         # inline keyboards
│   └── middlewares/       # user context middleware
├── requirements.txt
├── Dockerfile
└── .env.example
```

## Run locally (polling)

```bash
cd bot
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # set BOT_TOKEN and ADMIN_CHAT_IDS
python -m app.main
```

## Run in production (webhook)

```bash
BOT_MODE=webhook \
WEBHOOK_URL=https://api.example.com/bot/webhook \
WEBHOOK_SECRET=$(openssl rand -hex 32) \
BOT_HOST=0.0.0.0 BOT_PORT=8080 \
python -m app.main
```

## Environment

| Var                  | Description                                     |
| -------------------- | ----------------------------------------------- |
| `BOT_TOKEN`          | Telegram Bot API token                          |
| `BOT_MODE`           | `polling` (default) or `webhook`                |
| `WEBHOOK_URL`        | Public webhook URL (webhook mode)               |
| `WEBHOOK_PATH`       | Path the bot listens on (default `/bot/webhook`)|
| `WEBHOOK_SECRET`     | X-Telegram-Bot-Api-Secret-Token value           |
| `API_BASE_URL`       | FastAPI backend URL                             |
| `API_ADMIN_TOKEN`    | Token for protected endpoints                   |
| `ADMIN_CHAT_IDS`     | Comma-separated Telegram IDs for notifications  |
| `BOT_HOST` / `BOT_PORT` | Webhook bind address (webhook mode)           |

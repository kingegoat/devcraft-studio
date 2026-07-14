# Contributing to devcraft-studio

Thanks for your interest. This document explains how to set up the project locally, run tests, and submit changes.

## Quick start

You need Python 3.12+ and Node.js 18+ (only for linting).

```bash
git clone https://github.com/kingegoat/devcraft-studio.git
cd devcraft-studio

# Backend
cd api
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env  # edit if needed
pytest -v             # 8 tests, should all pass
uvicorn app.main:app --reload --port 8000

# Bot (separate terminal)
cd ../bot
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # set BOT_TOKEN, ADMIN_CHAT_IDS, API_BASE_URL
python -m app.main

# Site
cd ../site
python3 -m http.server 5173
# open http://localhost:5173
```

## Development workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Make your changes — one logical change per PR
4. Run tests and linters (must pass):
   ```bash
   cd api && pytest -v
   ```
5. Commit using [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` new feature
   - `fix:` bug fix
   - `docs:` documentation only
   - `refactor:` neither fixes a bug nor adds a feature
   - `chore:` tooling, dependencies
6. Push and open a Pull Request — fill in the PR template

## Project layout

```
devcraft-studio/
├── site/      # Vanilla HTML/CSS/JS landing page
├── api/       # FastAPI backend
├── bot/       # Telegram bot on aiogram 3
└── infra/     # docker-compose for production
```

See [README.md](README.md) for details.

## Code style

| Area | Convention |
| ---- | ---------- |
| Python | PEP 8, type hints everywhere, async-first |
| HTML | Semantic, one `<h1>` per page, ARIA where needed |
| CSS | Mobile-first, custom properties for tokens, no preprocessors |
| JS | Vanilla ES2024+, no frameworks, no bundlers |
| Bot | aiogram 3 with FSM, one feature per handler |

### Imports

```python
# Good
from app.models.lead import Lead
from app.services.leads import LeadsService

# Avoid
from app.models import *  # never
```

### Naming

- Files and functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Bot callbacks: `prefix:action` (e.g. `svc:landing`, `lead:cancel`)

## Testing

### Backend

```bash
cd api
pytest -v
```

Currently 8 tests covering health, lead CRUD, admin auth, and catalog seeding.

### Bot

Bot tests are manual. After changes:

1. Start bot and API
2. Send `/start` in Telegram
3. Walk through the full FSM (service → description → email)
4. Verify lead appears via `curl http://localhost:8000/api/leads -H "Authorization: Bearer $ADMIN_TOKEN"`

## Adding translations

- Site: edit `site/i18n/{ru,en,de}.json`
- Bot: edit `bot/app/locales/ru.json`

Keep keys identical across all dictionaries. Use dot notation in HTML/JS (`data-i18n="hero.title1"`).

## Adding a service / lead field

1. Add column to `api/app/models/`
2. Add field to `api/app/schemas.py`
3. Update seed if needed in `api/app/seed.py`
4. Update tests in `api/tests/`
5. Update README endpoints table

## Reporting bugs

Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md). Include:

- What you did
- What you expected
- What actually happened
- Environment (OS, Python version, etc.)
- Logs / screenshots

## Suggesting features

Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md).

## Security

See [SECURITY.md](SECURITY.md). **Do not** open public issues for security bugs — use the private channel.

## License

By contributing you agree your contributions will be licensed under the [MIT License](LICENSE).

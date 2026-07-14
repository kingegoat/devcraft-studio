# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-15

### Added

- Marketing site (`site/`) — vanilla HTML5/CSS3/JS, mobile-first responsive
  - Multi-language: RU / EN / DE dictionaries in `site/i18n/`
  - Dark / light theme with `localStorage` persistence
  - i18n switcher, intersection-observer reveals, accessible (ARIA, reduced-motion)
  - ~24 KB HTML, zero JavaScript dependencies
- FastAPI backend (`api/`)
  - Async SQLAlchemy 2.0 with Pydantic v2 validation
  - Endpoints: `/api/lead`, `/api/leads`, `/api/leads/{id}`, `/api/services`, `/api/health`, `/api/docs`
  - Admin auth via bearer token
  - OpenAPI docs auto-generated
  - 8 unit tests (pytest-asyncio)
  - SQLite default, PostgreSQL via `DATABASE_URL` env var (no code changes)
- Telegram bot (`bot/`)
  - aiogram 3 with FSM lead intake (service → description → email → done)
  - Inline keyboards with `❌ Отмена` button on every prompt
  - `/cancel` and `/exit` commands escape from any FSM step
  - `/contacts` and `/help` commands
  - Admin notifications (best-effort)
  - Polling mode by default, webhook-ready
- DevOps (`infra/`)
  - `docker-compose.yml` orchestrating api + bot + PostgreSQL + Nginx
  - Single-port deployment via Nginx reverse proxy
  - `deploy.sh` for one-command production rollouts
- Documentation
  - Architecture diagram in README
  - Per-component READMEs (`api/README.md`, `bot/README.md`)
  - MIT license

### Notes

This is the initial public release. The project serves as a reference for
the same stack I ship for clients — landing pages, Telegram bots, and
FastAPI web services.

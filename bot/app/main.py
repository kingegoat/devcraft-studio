"""Bot entry point — wires dispatcher, registers routers and middlewares."""
from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .api_client import api
from .config import get_settings
from .handlers import about, common, contact, language, portfolio, services
from .middlewares import UserContextMiddleware
from .store import UserStore


logger = logging.getLogger(__name__)


def build_dispatcher(store: UserStore) -> Dispatcher:
    dp = Dispatcher()
    dp.message.middleware(UserContextMiddleware(store))
    dp.callback_query.middleware(UserContextMiddleware(store))

    dp.include_routers(
        common.router,
        language.router,
        services.router,
        portfolio.router,
        about.router,
        contact.router,
    )
    return dp


async def _run_polling(bot: Bot, dp: Dispatcher) -> None:
    logger.info("Starting in polling mode…")
    await dp.start_polling(bot)


async def _run_webhook(bot: Bot, dp: Dispatcher) -> None:
    from aiohttp import web

    settings = get_settings()
    app = web.Application()

    async def webhook_handler(request: web.Request) -> web.Response:
        if settings.webhook_secret:
            header = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
            if header != settings.webhook_secret:
                return web.Response(status=403)
        update = await request.json()
        await dp.feed_webhook_update(bot, update)
        return web.Response(text="ok")

    async def internal_notify(request: web.Request) -> web.Response:
        """Receive lead notifications from the API and forward to admins."""
        payload = await request.json()
        lead = payload.get("lead", {})
        text = (
            f"📩 *New lead #{lead.get('id', '?')}* (lang: {lead.get('lang', 'ru')})\n\n"
            f"👤 {lead.get('name', '?')}\n"
            f"📧 {lead.get('email', '?')}\n"
            f"🛠 {lead.get('service', '?')}\n"
            f"💬 {lead.get('message', '')}"
        )
        for admin_id in settings.admin_ids:
            try:
                await bot.send_message(admin_id, text, parse_mode=ParseMode.MARKDOWN)
            except Exception:  # noqa: BLE001
                pass
        return web.Response(text="ok")

    app.router.add_post(settings.webhook_path, webhook_handler)
    app.router.add_post("/internal/notify", internal_notify)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, settings.bot_host, settings.bot_port)
    await site.start()
    logger.info("Webhook server listening on %s:%s", settings.bot_host, settings.bot_port)

    # Block forever
    await asyncio.Event().wait()


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    settings = get_settings()
    if not settings.bot_token:
        raise SystemExit("BOT_TOKEN is required")

    bot = Bot(
        settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
    )
    store = UserStore(Path("data/users.json"))
    dp = build_dispatcher(store)

    try:
        if settings.bot_mode == "webhook":
            if settings.webhook_url:
                await bot.set_webhook(
                    settings.webhook_url,
                    secret_token=settings.webhook_secret or None,
                )
            await _run_webhook(bot, dp)
        else:
            await _run_polling(bot, dp)
    finally:
        await api.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")

"""Bot entry point — wires dispatcher, registers routers and middlewares."""
from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .api_client import api
from .config import get_settings
from .handlers import common, contact

logger = logging.getLogger(__name__)


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
    dp = Dispatcher()

    # Order matters: contact.router is registered LAST so its fallback
    # (catch-all text handler) doesn't shadow /start.
    dp.include_routers(common.router, contact.router)

    try:
        logger.info("Starting bot in polling mode…")
        await dp.start_polling(bot)
    finally:
        await api.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")

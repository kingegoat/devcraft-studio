"""Services catalog handler."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.types import CallbackQuery

from ..i18n import i18n
from ..keyboards import back_kb, service_order_kb, services_kb
from ..config import get_settings

router = Router(name="services")


@router.callback_query(F.data == "menu:services")
async def cb_services(call: CallbackQuery, lang: str) -> None:
    await call.message.edit_text(
        i18n.t(lang, "services.title"),
        reply_markup=services_kb({"back": i18n.t(lang, "menu.back")}),
    )
    await call.answer()


@router.callback_query(F.data.startswith("svc:"))
async def cb_service_detail(call: CallbackQuery, lang: str) -> None:
    slug = call.data.split(":", 1)[1]
    # Prices are in cents in API; for bot display convert roughly
    prices = {"landing": "$300", "bot": "$500", "api": "$700"}
    titles = {"landing": "services.landing", "bot": "services.bot", "api": "services.api"}
    if slug not in titles:
        await call.answer("Unknown service", show_alert=True)
        return

    text = (
        f"*{i18n.t(lang, titles[slug] + '.title')}*\n\n"
        + i18n.t(lang, titles[slug] + ".text", price=prices[slug])
    )

    order_label = {
        "landing": i18n.t(lang, "services.landing.cta"),
        "bot": i18n.t(lang, "services.bot.cta"),
        "api": i18n.t(lang, "services.api.cta"),
    }[slug]

    await call.message.edit_text(
        text,
        reply_markup=service_order_kb(slug, {"order": order_label, "back": i18n.t(lang, "menu.back")}),
    )
    await call.answer()

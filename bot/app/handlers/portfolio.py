"""Portfolio handler — fetches projects from the API and renders them inline."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.types import CallbackQuery

from ..api_client import api
from ..i18n import i18n
from ..keyboards import back_kb

router = Router(name="portfolio")


@router.callback_query(F.data == "menu:portfolio")
async def cb_portfolio(call: CallbackQuery, lang: str) -> None:
    try:
        projects = await api.get_projects()
    except Exception:  # noqa: BLE001
        projects = []

    if not projects:
        await call.message.edit_text(
            i18n.t(lang, "portfolio.title"),
            reply_markup=back_kb({"back": i18n.t(lang, "menu.back")}),
        )
        await call.answer()
        return

    lines = [i18n.t(lang, "portfolio.title"), ""]
    for p in projects[:8]:
        url = p.get("repo_url") or p.get("demo_url") or ""
        lines.append(i18n.t(
            lang, "portfolio.item",
            title=p["title"],
            description=p["description"],
            stack=", ".join(p.get("stack", [])[:4]),
            url=url or "—",
        ))

    await call.message.edit_text(
        "\n\n".join(lines),
        reply_markup=back_kb({"back": i18n.t(lang, "menu.back")}),
    )
    await call.answer()

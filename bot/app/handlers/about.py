"""About / static info handler."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.types import CallbackQuery

from ..i18n import i18n
from ..keyboards import back_kb

router = Router(name="about")


@router.callback_query(F.data == "menu:about")
async def cb_about(call: CallbackQuery, lang: str) -> None:
    await call.message.edit_text(
        i18n.t(lang, "about.text"),
        reply_markup=back_kb({"back": i18n.t(lang, "menu.back")}),
    )
    await call.answer()

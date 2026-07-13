"""Language switch handler (also accessible from main menu later)."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.types import CallbackQuery

from ..i18n import i18n
from ..keyboards import language_kb

router = Router(name="language")


@router.callback_query(F.data == "menu:lang")
async def cb_change_language(call: CallbackQuery) -> None:
    await call.message.edit_text(
        i18n.t("ru", "start.choose_lang"),
        reply_markup=language_kb(),
    )
    await call.answer()

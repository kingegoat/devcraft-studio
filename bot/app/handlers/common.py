"""Common / language / menu handlers."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from ..i18n import i18n
from ..keyboards import language_kb, main_menu

router = Router(name="common")


@router.message(Command("start"))
async def cmd_start(message: Message, lang: str, store, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        i18n.t(lang, "start.choose_lang"),
        reply_markup=language_kb(),
    )


@router.callback_query(F.data.startswith("lang:"))
async def cb_set_language(call: CallbackQuery, store, state: FSMContext) -> None:
    new_lang = call.data.split(":", 1)[1]
    store.set_lang(call.from_user.id, new_lang)
    await state.clear()

    labels = {
        "services": i18n.t(new_lang, "menu.services"),
        "portfolio": i18n.t(new_lang, "menu.portfolio"),
        "contact": i18n.t(new_lang, "menu.contact"),
        "about": i18n.t(new_lang, "menu.about"),
    }
    await call.message.edit_text(
        i18n.t(new_lang, "start.welcome"),
        reply_markup=main_menu(new_lang, labels),
    )
    await call.answer()


@router.callback_query(F.data == "menu:home")
async def cb_home(call: CallbackQuery, lang: str, state: FSMContext) -> None:
    await state.clear()
    labels = {
        "services": i18n.t(lang, "menu.services"),
        "portfolio": i18n.t(lang, "menu.portfolio"),
        "contact": i18n.t(lang, "menu.contact"),
        "about": i18n.t(lang, "menu.about"),
    }
    await call.message.edit_text(
        i18n.t(lang, "start.welcome"),
        reply_markup=main_menu(lang, labels),
    )
    await call.answer()

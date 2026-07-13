"""Contact form / lead intake FSM."""
from __future__ import annotations

import re
from typing import Any

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from ..api_client import api
from ..config import get_settings
from ..i18n import i18n
from ..keyboards import back_kb

router = Router(name="contact")

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


class ContactForm(StatesGroup):
    waiting_name = State()
    waiting_email = State()
    waiting_message = State()


@router.callback_query(F.data == "menu:contact")
async def cb_contact(call: CallbackQuery, lang: str, state: FSMContext) -> None:
    await state.set_state(ContactForm.waiting_name)
    await call.message.edit_text(i18n.t(lang, "contact.ask_name"))
    await call.answer()


@router.callback_query(F.data.startswith("order:"))
async def cb_order(call: CallbackQuery, lang: str, state: FSMContext) -> None:
    """When user clicks 'order this service' on the services screen."""
    slug = call.data.split(":", 1)[1]
    await state.set_state(ContactForm.waiting_name)
    await state.update_data(service=slug)
    await call.message.edit_text(i18n.t(lang, "contact.ask_name"))
    await call.answer()


@router.message(ContactForm.waiting_name)
async def fsm_name(message: Message, lang: str, state: FSMContext) -> None:
    name = (message.text or "").strip()
    if len(name) < 2:
        await message.answer(i18n.t(lang, "contact.ask_name"))
        return
    await state.update_data(name=name)
    await state.set_state(ContactForm.waiting_email)
    await message.answer(i18n.t(lang, "contact.ask_email"))


@router.message(ContactForm.waiting_email)
async def fsm_email(message: Message, lang: str, state: FSMContext) -> None:
    email = (message.text or "").strip()
    if not EMAIL_RE.match(email):
        await message.answer(i18n.t(lang, "contact.invalid_email"))
        return
    await state.update_data(email=email)
    await state.set_state(ContactForm.waiting_message)
    await message.answer(i18n.t(lang, "contact.ask_message"))


@router.message(ContactForm.waiting_message)
async def fsm_message(message: Message, lang: str, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if len(text) < 5:
        await message.answer(i18n.t(lang, "contact.ask_message"))
        return

    data: dict[str, Any] = await state.get_data()
    service = data.get("service", "other")

    # Persist via API
    try:
        result = await api.create_lead({
            "name": data["name"],
            "email": data["email"],
            "service": service,
            "message": text,
            "source": "telegram",
            "lang": lang,
        })
        lead_id = result.get("id", "?")
    except Exception:  # noqa: BLE001
        lead_id = "?"

    # Notify admins (best-effort, no failure side-effect on user)
    await _notify_admins(message.bot, lead_id, data, service, text, lang)

    await message.answer(
        i18n.t(lang, "contact.thanks", name=data["name"], id=lead_id),
        reply_markup=back_kb({"back": i18n.t(lang, "menu.back")}),
    )
    await state.clear()


async def _notify_admins(bot: Bot, lead_id: Any, data: dict, service: str, message: str, lang: str) -> None:
    settings = get_settings()
    if not settings.admin_ids:
        return
    text = (
        f"📩 *New lead #{lead_id}* (lang: {lang})\n\n"
        f"👤 {data.get('name', '?')}\n"
        f"📧 {data.get('email', '?')}\n"
        f"🛠 {service}\n"
        f"💬 {message}"
    )
    for admin_id in settings.admin_ids:
        try:
            await bot.send_message(admin_id, text, parse_mode="Markdown")
        except Exception:  # noqa: BLE001
            pass

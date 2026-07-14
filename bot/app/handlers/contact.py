"""Lead intake FSM — one simple flow: service → description → email → done."""
from __future__ import annotations

import re
from typing import Any

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from ..api_client import api
from ..config import get_settings
from ..keyboards import service_picker_kb
from ..states import LeadForm

router = Router(name="contact")

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")


@router.callback_query(F.data.startswith("svc:"))
async def cb_pick_service(call: CallbackQuery, state: FSMContext) -> None:
    """User picked a service from /start menu."""
    service = call.data.split(":", 1)[1]
    await state.update_data(service=service)
    await state.set_state(LeadForm.description)
    await call.message.edit_text(
        "📝 *Опишите задачу кратко*\n\n"
        "Что нужно сделать, какие сроки, есть ли примеры или референсы."
    )
    await call.answer()


@router.callback_query(F.data == "lead:cancel")
async def cb_cancel(call: CallbackQuery, state: FSMContext) -> None:
    """Cancel from any FSM step."""
    await state.clear()
    await call.message.edit_text(
        "Отменено. Если что — /start",
        reply_markup=service_picker_kb(),
    )
    await call.answer()


@router.message(LeadForm.description)
async def fsm_description(message: Message, state: FSMContext) -> None:
    desc = (message.text or "").strip()
    if len(desc) < 5:
        await message.answer("Пара слов точно нужно — что сделать?")
        return
    await state.update_data(description=desc)
    await state.set_state(LeadForm.email)
    await message.answer("📧 *Email для связи:*")


@router.message(LeadForm.email)
async def fsm_email(message: Message, state: FSMContext) -> None:
    email = (message.text or "").strip()
    if not EMAIL_RE.match(email):
        await message.answer("Похоже, email некорректный. Попробуйте ещё раз:")
        return

    data: dict[str, Any] = await state.get_data()
    user = message.from_user
    name = (user.first_name or "") + (f" {user.last_name}" if user.last_name else "")
    name = name.strip() or "Telegram user"

    # Persist via API
    lead_id: Any = "?"
    try:
        result = await api.create_lead({
            "name": name,
            "email": email,
            "service": data["service"],
            "message": data["description"],
            "source": "telegram",
            "lang": "ru",
        })
        lead_id = result.get("id", "?")
    except Exception:  # noqa: BLE001
        pass

    # Notify admins (best effort)
    await _notify_admins(message.bot, lead_id, name, email, user, data)

    await message.answer(
        f"✅ *Заявка #{lead_id} принята!*\n\n"
        f"Свяжусь с вами по email в течение 2 часов.\n\n"
        f"Если что-то ещё — /start",
    )
    await state.clear()


async def _notify_admins(bot: Bot, lead_id: Any, name: str, email: str,
                         user, data: dict) -> None:
    settings = get_settings()
    if not settings.admin_ids:
        return

    service_labels = {
        "landing": "🌐 Лендинг / сайт",
        "bot": "🤖 Telegram-бот",
        "api": "⚙️ API / backend",
        "other": "📝 Другое",
    }
    service_label = service_labels.get(data.get("service", ""), data.get("service", ""))

    text = (
        f"📩 *Новая заявка #{lead_id}*\n\n"
        f"Услуга: {service_label}\n"
        f"Имя: {name}\n"
        f"Email: {email}\n"
        f"Username: @{user.username or '—'} (id {user.id})\n\n"
        f"💬 _{data.get('description', '')}_"
    )

    for admin_id in settings.admin_ids:
        try:
            await bot.send_message(admin_id, text, parse_mode="Markdown")
        except Exception:  # noqa: BLE001
            pass


@router.message()
async def fallback(message: Message, state: FSMContext) -> None:
    """Catch-all: any text outside FSM jumps to /start."""
    current = await state.get_state()
    if current is not None:
        return  # let FSM handlers do their thing
    await cmd_start(message, state)

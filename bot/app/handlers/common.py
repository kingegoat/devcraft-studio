"""Common handlers — /start with simple service picker, /contacts."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from ..keyboards import contacts_kb, service_picker_kb
from ..states import LeadForm

router = Router(name="common")


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext) -> None:
    """Single screen: what do you need?"""
    await state.clear()
    await message.answer(
        "👋 *DevCraft Studio*\n\n"
        "Full-stack разработка: лендинги, Telegram-боты, веб-сервисы на FastAPI.\n\n"
        "Что нужно сделать?",
        reply_markup=service_picker_kb(),
    )


@router.callback_query(F.data == "menu:home")
async def cb_home(call: CallbackQuery, state: FSMContext) -> None:
    """Restart the flow from scratch."""
    await state.clear()
    await call.message.edit_text(
        "👋 *DevCraft Studio*\n\n"
        "Что нужно сделать?",
        reply_markup=service_picker_kb(),
    )
    await call.answer()


@router.callback_query(F.data == "menu:contacts")
async def cb_contacts(call: CallbackQuery) -> None:
    await call.message.edit_text(
        "📞 *Контакты*\n\n"
        "Telegram: @kingegoat\n"
        "Email: hello@devcraft.studio\n"
        "GitHub: github.com/kingegoat\n"
        "Сайт: github.com/kingegoat/devcraft-studio",
        reply_markup=contacts_kb(),
    )
    await call.answer()


@router.message(Command("contacts"))
async def cmd_contacts(message: Message) -> None:
    await message.answer(
        "📞 *Контакты*\n\n"
        "Telegram: @kingegoat\n"
        "Email: hello@devcraft.studio\n"
        "GitHub: github.com/kingegoat\n"
        "Сайт: github.com/kingegoat/devcraft-studio",
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "ℹ️ *Помощь*\n\n"
        "/start — оставить заявку\n"
        "/contacts — мои контакты\n"
        "/help — эта справка\n\n"
        "Или просто напишите что нужно — разберёмся.",
    )

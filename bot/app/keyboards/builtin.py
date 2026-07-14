"""Inline keyboards — minimal set for the simplified bot."""
from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def service_picker_kb() -> InlineKeyboardMarkup:
    """Shown on /start — one clear question: what do you need?"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Лендинг / сайт",  callback_data="svc:landing")],
        [InlineKeyboardButton(text="🤖 Telegram-бот",    callback_data="svc:bot")],
        [InlineKeyboardButton(text="⚙️ API / backend",   callback_data="svc:api")],
        [InlineKeyboardButton(text="📝 Другое",          callback_data="svc:other")],
        [InlineKeyboardButton(text="📞 Контакты",        callback_data="menu:contacts")],
    ])


def contacts_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu:home")],
    ])

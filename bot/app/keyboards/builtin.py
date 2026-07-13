"""Inline / reply keyboards for the bot."""
from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu(lang: str, labels: dict[str, str]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=labels["services"], callback_data="menu:services"),
            InlineKeyboardButton(text=labels["portfolio"], callback_data="menu:portfolio"),
        ],
        [
            InlineKeyboardButton(text=labels["contact"], callback_data="menu:contact"),
            InlineKeyboardButton(text=labels["about"], callback_data="menu:about"),
        ],
    ])


def services_kb(labels: dict[str, str]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Landing", callback_data="svc:landing")],
        [InlineKeyboardButton(text="🤖 Telegram bot", callback_data="svc:bot")],
        [InlineKeyboardButton(text="⚙️ API / backend", callback_data="svc:api")],
        [InlineKeyboardButton(text=labels["back"], callback_data="menu:home")],
    ])


def back_kb(labels: dict[str, str], target: str = "menu:home") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=labels["back"], callback_data=target)]
    ])


def language_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
            InlineKeyboardButton(text="🇩🇪 Deutsch", callback_data="lang:de"),
        ]
    ])


def service_order_kb(slug: str, labels: dict[str, str]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=labels["order"], callback_data=f"order:{slug}")],
        [InlineKeyboardButton(text=labels["back"], callback_data="menu:services")],
    ])

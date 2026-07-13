"""Per-chat middleware that injects `lang` and `store` into handler kwargs."""
from __future__ import annotations

from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from ..store import UserStore


class UserContextMiddleware(BaseMiddleware):
    def __init__(self, store: UserStore) -> None:
        self.store = store
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if user is not None:
            data["lang"] = self.store.get_lang(user.id)
            data["store"] = self.store
        return await handler(event, data)

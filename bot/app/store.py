"""User-level helpers: persist per-chat state (lang, current flow)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional


class UserStore:
    """Trivial JSON-on-disk user store.

    Replace with Redis/Postgres in production — interface stays the same.
    """

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("{}", encoding="utf-8")
        self._data: dict[int, dict] = self._load()

    def _load(self) -> dict[int, dict]:
        raw = json.loads(self.path.read_text(encoding="utf-8") or "{}")
        return {int(k): v for k, v in raw.items()}

    def _flush(self) -> None:
        self.path.write_text(
            json.dumps(self._data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _bucket(self, user_id: int) -> dict:
        return self._data.setdefault(user_id, {"lang": "ru", "fsm": None})

    def get_lang(self, user_id: int) -> str:
        return self._bucket(user_id).get("lang", "ru")

    def set_lang(self, user_id: int, lang: str) -> None:
        self._bucket(user_id)["lang"] = lang
        self._flush()

    def get_fsm(self, user_id: int) -> Optional[str]:
        return self._bucket(user_id).get("fsm")

    def set_fsm(self, user_id: int, state: Optional[str]) -> None:
        bucket = self._bucket(user_id)
        if state is None:
            bucket.pop("fsm", None)
        else:
            bucket["fsm"] = state
        self._flush()

    def get_fsm_data(self, user_id: int) -> dict:
        return self._bucket(user_id).get("fsm_data", {})

    def set_fsm_data(self, user_id: int, data: dict) -> None:
        self._bucket(user_id)["fsm_data"] = data
        self._flush()

    def clear_fsm(self, user_id: int) -> None:
        bucket = self._bucket(user_id)
        bucket.pop("fsm", None)
        bucket.pop("fsm_data", None)
        self._flush()

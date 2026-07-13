"""Lightweight i18n for the bot. Loads JSON dictionaries on demand."""
import json
from pathlib import Path
from typing import Dict


I18N_DIR = Path(__file__).resolve().parent / "locales"


class I18n:
    """Minimal i18n helper for bot messages."""

    DEFAULT_LANG = "ru"
    SUPPORTED = ("ru", "en", "de")

    def __init__(self) -> None:
        self._cache: Dict[str, dict] = {}

    def load(self, lang: str) -> dict:
        lang = lang if lang in self.SUPPORTED else self.DEFAULT_LANG
        if lang not in self._cache:
            path = I18N_DIR / f"{lang}.json"
            with path.open(encoding="utf-8") as f:
                self._cache[lang] = json.load(f)
        return self._cache[lang]

    def t(self, lang: str, key: str, **kwargs) -> str:
        """Translate a dot-path key, format placeholders."""
        d = self.load(lang)
        node: object = d
        for part in key.split("."):
            if isinstance(node, dict):
                node = node.get(part)
            else:
                node = None
            if node is None:
                return key
        if isinstance(node, str):
            try:
                return node.format(**kwargs)
            except (KeyError, IndexError):
                return node
        return str(node)


i18n = I18n()

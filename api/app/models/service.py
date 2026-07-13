"""
Service catalog — populated by seed data on startup, exposed via /api/services.
"""
from typing import List, Optional

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class Service(Base):
    __tablename__ = "services"

    id:           Mapped[int]      = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug:         Mapped[str]      = mapped_column(String(64), unique=True, index=True)
    title:        Mapped[str]      = mapped_column(String(160), nullable=False)
    description:  Mapped[str]      = mapped_column(String(600), nullable=False)
    features:     Mapped[str]      = mapped_column(String(600), nullable=False)  # comma-separated
    price_from:   Mapped[int]      = mapped_column(Integer, default=0)            # in cents
    currency:     Mapped[str]      = mapped_column(String(8), default="USD")
    badge:        Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    order:        Mapped[int]      = mapped_column(Integer, default=0)
    is_active:    Mapped[bool]     = mapped_column(default=True)

    def feature_list(self) -> List[str]:
        return [f.strip() for f in self.features.split(",") if f.strip()]

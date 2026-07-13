"""
Lead model — captures contact-form submissions from the marketing site.
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class Lead(Base):
    __tablename__ = "leads"

    id:           Mapped[int]      = mapped_column(primary_key=True, autoincrement=True)
    name:         Mapped[str]      = mapped_column(String(120), nullable=False)
    email:        Mapped[str]      = mapped_column(String(254), nullable=False, index=True)
    service:      Mapped[str]      = mapped_column(String(40),  nullable=False, index=True)
    message:      Mapped[str]      = mapped_column(Text,         nullable=False)
    source:       Mapped[str]      = mapped_column(String(40),  default="site")
    lang:         Mapped[str]      = mapped_column(String(8),   default="ru")
    ip:           Mapped[Optional[str]] = mapped_column(String(64),  nullable=True)
    user_agent:   Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    status:       Mapped[str]      = mapped_column(String(20),  default="new")  # new|contacted|won|lost
    notes:        Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at:   Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:   Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        return f"<Lead #{self.id} {self.email!r} service={self.service}>"

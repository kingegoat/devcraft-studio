"""
Project / portfolio item model.
"""
from typing import List, Optional

from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class Project(Base):
    __tablename__ = "projects"

    id:           Mapped[int]      = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug:         Mapped[str]      = mapped_column(String(64), unique=True, index=True)
    title:        Mapped[str]      = mapped_column(String(160), nullable=False)
    description:  Mapped[str]      = mapped_column(Text, nullable=False)
    tag:          Mapped[str]      = mapped_column(String(40), nullable=False)
    stack:        Mapped[str]      = mapped_column(String(300), nullable=False)  # comma-separated
    repo_url:     Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    demo_url:     Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    cover_color:  Mapped[str]      = mapped_column(String(20), default="#7c5cff")
    order:        Mapped[int]      = mapped_column(Integer, default=0)
    is_active:    Mapped[bool]     = mapped_column(default=True)

    def stack_list(self) -> List[str]:
        return [s.strip() for s in self.stack.split(",") if s.strip()]

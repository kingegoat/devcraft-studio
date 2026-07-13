"""
Pydantic v2 schemas for request/response validation.
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


# ============================== Lead ==============================
class LeadCreate(BaseModel):
    """Inbound payload from the marketing site contact form."""
    name:    str = Field(..., min_length=2, max_length=120)
    email:   EmailStr
    service: str = Field(..., min_length=2, max_length=40)
    message: str = Field(..., min_length=10, max_length=4000)
    source:  Optional[str] = Field(default="site", max_length=40)
    lang:    Optional[str] = Field(default="ru", max_length=8)


class LeadOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    service: str
    message: str
    source: str
    lang: str
    status: str
    created_at: datetime


class LeadStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(new|contacted|won|lost)$")
    notes:  Optional[str] = None


# ============================== Service ==============================
class ServiceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    description: str
    features: List[str]
    price_from: int
    currency: str
    badge: Optional[str] = None


# ============================== Project ==============================
class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    description: str
    tag: str
    stack: List[str]
    repo_url: Optional[str] = None
    demo_url: Optional[str] = None
    cover_color: str


# ============================== Health ==============================
class HealthOut(BaseModel):
    status: str
    version: str
    time: datetime

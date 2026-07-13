"""
Public projects / portfolio endpoint.
"""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.project import Project
from ..schemas import ProjectOut

router = APIRouter(prefix="/api/projects", tags=["catalog"])


@router.get("", response_model=list[ProjectOut])
async def list_projects(db: AsyncSession = Depends(get_db)) -> list[ProjectOut]:
    stmt = select(Project).where(Project.is_active.is_(True)).order_by(Project.order)
    rows = (await db.execute(stmt)).scalars().all()
    return [
        ProjectOut(
            id=p.id,
            slug=p.slug,
            title=p.title,
            description=p.description,
            tag=p.tag,
            stack=p.stack_list(),
            repo_url=p.repo_url,
            demo_url=p.demo_url,
            cover_color=p.cover_color,
        )
        for p in rows
    ]

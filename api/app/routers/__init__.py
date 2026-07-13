"""
HTTP routers — thin controllers wired into the FastAPI app.
"""
from .health import router as health_router
from .leads import router as leads_router
from .projects import router as projects_router
from .services import router as services_router

__all__ = ["health_router", "leads_router", "projects_router", "services_router"]

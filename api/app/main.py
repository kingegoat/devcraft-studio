"""
FastAPI application factory + middleware + lifespan.
"""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .database import AsyncSessionLocal, init_db
from .routers import health_router, leads_router, projects_router, services_router
from .seed import seed_catalog


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown hooks."""
    settings = get_settings()
    await init_db()
    async with AsyncSessionLocal() as db:
        await seed_catalog(db)
    yield
    # shutdown: dispose engine
    from .database import engine
    await engine.dispose()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        lifespan=lifespan,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(leads_router)
    app.include_router(services_router)
    app.include_router(projects_router)

    # Optional: serve the marketing site as static files (single-port deploy)
    if settings.serve_site and settings.site_dir.exists():
        app.mount(
            "/",
            StaticFiles(directory=str(settings.site_dir), html=True),
            name="site",
        )
    else:
        @app.get("/")
        async def index() -> JSONResponse:
            return JSONResponse({
                "service": settings.api_title,
                "version": settings.api_version,
                "docs": "/api/docs",
                "endpoints": [
                    "POST /api/lead",
                    "GET  /api/services",
                    "GET  /api/projects",
                    "GET  /api/health",
                ],
            })

    return app


app = create_app()

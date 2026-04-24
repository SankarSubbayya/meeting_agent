from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import get_settings
from app.db.session import init_db
from app.routers import actions, admin, meetings, read_tools


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    app.include_router(read_tools.router)
    app.include_router(actions.router)
    app.include_router(meetings.router)
    app.include_router(admin.router)

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app


app = create_app()

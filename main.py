from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.books import router as books_router
from app.api.routes.recommendations import router as recommendations_router
from app.api.routes.summaries import router as summary_router
from app.core.config import settings
from app.core.dependencies import engine
from app.db import models  # noqa: F401
from app.db.base import Base

app = FastAPI(title=settings.app_name)

app.include_router(auth_router)
app.include_router(books_router)
app.include_router(recommendations_router)
app.include_router(summary_router)


@app.on_event("startup")
async def startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

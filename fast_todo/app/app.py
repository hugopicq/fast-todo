import logging
import contextlib
from fastapi import FastAPI, Request

from fast_todo.app.health import router as health_router
from fast_todo.app.endpoints.tasks import router as tasks_router
from fast_todo.app.endpoints.users import router as users_router

from fast_todo.app.pg_pool import PGPool

logger = logging.getLogger("uvicorn")

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Opening database connection")
    async with PGPool.get_connection() as connection:
        try:
            await connection.execute("SELECT 1")
        except Exception as e:
            logger.exception("Error pinging database", exc_info=True)
            raise e
    logger.info("Database connection opened...")
    yield
    logger.info("Closing database connection...")
    await PGPool.close_connection()
    logger.info("Database connection closed...")

def create_app() -> FastAPI:
    app = FastAPI(
        title="TODO API",
        description="API built with FastAPI for a todo app",
        version="0.1",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    app.include_router(health_router)
    app.include_router(tasks_router)
    app.include_router(users_router)

    return app

app = create_app()

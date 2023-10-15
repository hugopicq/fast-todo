import logging

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from fast_todo.app.pg_pool import PGPool

logger = logging.getLogger("uvicorn")

router = APIRouter(prefix="/health", tags=["health"])


class OKStatusResponse(BaseModel):
    status: str = "OK"


@router.get("/")
async def health() -> OKStatusResponse:
    """
    Health endpoint returning status: OK if the database can be reached

    Parameters
    ----------
    None

    Returns
    -------
    if healthy: {status: OK}, otherwise it raises a 500 error

    Raises
    ------
    HTTPException: 500 if there is a problem with the db
    """

    logger.info("Health checking...")
    logger.info("Pinging database...")

    async with PGPool.get_connection() as connection:
        try:
            await connection.execute("SELECT 1")
        except Exception as e:
            logger.exception("Error pinging database", exc_info=True)
            raise HTTPException(status_code=500, detail="Error pinging database")

    return OKStatusResponse()

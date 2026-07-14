from fastapi import APIRouter, Depends

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db

router = APIRouter()


@router.get("/db-check", tags=["Database"])
async def database_check(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(text("SELECT 1"))
    value = result.scalar()

    return {
        "database": "connected",
        "result": value,
    }
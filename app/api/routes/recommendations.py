from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.db.crud.books import list_books

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("")
async def get_recommendations(db: AsyncSession = Depends(get_db)):
    books = await list_books(db)
    return [
        {
            "id": book.id,
            "title": book.title,
            "genre": book.genre,
            "summary": book.summary,
        }
        for book in books[:5]
    ]

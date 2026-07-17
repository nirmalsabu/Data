import inspect
from typing import Callable, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Book, Review
from app.schemas.book import BookCreate, BookUpdate


async def create_book(db: AsyncSession, book_data: BookCreate, summary_service: Callable[[str], str]) -> Book:
    summary_result = summary_service(book_data.content or book_data.title)
    if inspect.isawaitable(summary_result):
        summary = await summary_result
    else:
        summary = summary_result

    book = Book(
        title=book_data.title,
        author=book_data.author,
        genre=book_data.genre,
        year_published=book_data.year_published,
        content=book_data.content,
        summary=summary,
    )
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book


async def list_books(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Book]:
    result = await db.execute(select(Book).options(selectinload(Book.reviews)).offset(skip).limit(limit))
    return list(result.scalars().all())


async def get_book_by_id(db: AsyncSession, book_id: int) -> Optional[Book]:
    result = await db.execute(select(Book).where(Book.id == book_id).options(selectinload(Book.reviews)))
    return result.scalar_one_or_none()


async def update_book(db: AsyncSession, book_id: int, book_update: BookUpdate) -> Optional[Book]:
    book = await get_book_by_id(db, book_id)
    if not book:
        return None
    for field, value in book_update.model_dump(exclude_unset=True).items():
        setattr(book, field, value)
    await db.commit()
    await db.refresh(book)
    return book


async def delete_book(db: AsyncSession, book_id: int) -> bool:
    book = await get_book_by_id(db, book_id)
    if not book:
        return False
    await db.delete(book)
    await db.commit()
    return True

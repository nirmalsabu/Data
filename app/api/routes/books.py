from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_summary_service
from app.db.crud.books import create_book, delete_book, get_book_by_id, list_books, update_book
from app.db.crud.reviews import create_review, get_review_summary, list_reviews
from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.schemas.review import ReviewCreate, ReviewRead
from app.services.summary_service import SummaryService

router = APIRouter(prefix="/books", tags=["books"])


@router.post("", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def add_book(
    book_data: BookCreate,
    db: AsyncSession = Depends(get_db),
    summary_service: SummaryService = Depends(get_summary_service),
):
    return await create_book(db, book_data, summary_service.generate_summary)


@router.get("", response_model=list[BookRead])
async def list_book_endpoint(db: AsyncSession = Depends(get_db)):
    return await list_books(db)


@router.get("/{book_id}", response_model=BookRead)
async def get_book_endpoint(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookRead)
async def update_book_endpoint(book_id: int, book_update: BookUpdate, db: AsyncSession = Depends(get_db)):
    book = await update_book(db, book_id, book_update)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_endpoint(book_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")


@router.post("/{book_id}/reviews", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
async def add_review(book_id: int, review_data: ReviewCreate, db: AsyncSession = Depends(get_db)):
    book = await get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return await create_review(db, book_id, review_data)


@router.get("/{book_id}/reviews", response_model=list[ReviewRead])
async def get_reviews(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return await list_reviews(db, book_id)


@router.get("/{book_id}/summary")
async def get_book_summary(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    average_rating, reviews = await get_review_summary(db, book_id)
    return {"book_id": book.id, "title": book.title, "summary": book.summary, "average_rating": average_rating, "review_count": len(reviews)}

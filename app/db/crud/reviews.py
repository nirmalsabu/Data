from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Book, Review
from app.schemas.review import ReviewCreate


async def create_review(db: AsyncSession, book_id: int, review_data: ReviewCreate) -> Review:
    review = Review(
        book_id=book_id,
        user_id=review_data.user_id,
        review_text=review_data.review_text,
        rating=review_data.rating,
    )
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review


async def list_reviews(db: AsyncSession, book_id: int) -> list[Review]:
    result = await db.execute(select(Review).where(Review.book_id == book_id))
    return list(result.scalars().all())


async def get_review_summary(db: AsyncSession, book_id: int) -> tuple[Optional[float], list[Review]]:
    reviews = await list_reviews(db, book_id)
    if not reviews:
        return None, []
    average_rating = sum(review.rating for review in reviews) / len(reviews)
    return average_rating, reviews

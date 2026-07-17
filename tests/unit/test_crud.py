import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.crud.auth import authenticate_user, create_user
from app.db.crud.books import create_book, delete_book, get_book_by_id, list_books, update_book
from app.db.crud.reviews import create_review, list_reviews
from app.schemas.auth import UserCreate
from app.schemas.book import BookCreate, BookUpdate
from app.schemas.review import ReviewCreate


@pytest.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as db:
        yield db

    await engine.dispose()


@pytest.mark.asyncio
async def test_create_and_fetch_book(session):
    book = await create_book(
        session,
        BookCreate(
            title="Dune",
            author="Frank Herbert",
            genre="Science Fiction",
            year_published=1965,
            content="A desert planet and prophecy.",
        ),
        summary_service=lambda content: f"Summary for {content}",
    )

    fetched = await get_book_by_id(session, book.id)
    assert fetched is not None
    assert fetched.title == "Dune"
    assert fetched.summary == "Summary for A desert planet and prophecy."


@pytest.mark.asyncio
async def test_update_and_delete_book(session):
    created = await create_book(
        session,
        BookCreate(title="1984", author="George Orwell", genre="Dystopian", year_published=1949, content="Totalitarian state."),
        summary_service=lambda content: "summary",
    )

    updated = await update_book(session, created.id, BookUpdate(title="Nineteen Eighty-Four"))
    assert updated.title == "Nineteen Eighty-Four"

    deleted = await delete_book(session, created.id)
    assert deleted is True
    assert await get_book_by_id(session, created.id) is None


@pytest.mark.asyncio
async def test_create_review_and_list_reviews(session):
    book = await create_book(
        session,
        BookCreate(title="Clean Code", author="Robert C. Martin", genre="Programming", year_published=2008, content="Refactoring and testing."),
        summary_service=lambda content: "summary",
    )

    review = await create_review(
        session,
        book.id,
        ReviewCreate(user_id="user-1", review_text="Excellent guidance", rating=5),
    )

    reviews = await list_reviews(session, book.id)
    assert len(reviews) == 1
    assert review.rating == 5
    assert reviews[0].review_text == "Excellent guidance"


@pytest.mark.asyncio
async def test_authentication_flow(session):
    created = await create_user(session, UserCreate(username="alice", email="alice@example.com", password="secret123"))
    authenticated = await authenticate_user(session, created.username, "secret123")
    assert authenticated is not None
    assert authenticated.username == "alice"

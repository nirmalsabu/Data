from pydantic import BaseModel, Field


class ReviewBase(BaseModel):
    user_id: str = Field(..., min_length=1)
    review_text: str = Field(..., min_length=1)
    rating: int = Field(..., ge=1, le=5)


class ReviewCreate(ReviewBase):
    pass


class ReviewRead(ReviewBase):
    id: int
    book_id: int

    class Config:
        from_attributes = True

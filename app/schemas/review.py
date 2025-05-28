from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime
import enum

class BookingReviewBase(BaseModel):
    rating: float = Field(..., ge=0, le=5)
    comment: Optional[str] = None

class ReviewCreate(BookingReviewBase):
    booking_id: UUID

class ReviewResponse(BookingReviewBase):
    id: UUID
    provider_id: UUID
    client_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class ReviewListResponse(BaseModel):
    total: int
    average_rating: float
    items: List[ReviewResponse]
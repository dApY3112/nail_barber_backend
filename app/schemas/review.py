from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime
import enum

class ReviewBase(BaseModel):
    rating: float = Field(..., ge=0, le=5)
    comment: Optional[str] = None

class ReviewCreate(BaseModel):
    provider_id: UUID
    rating: float = Field(..., ge=0, le=5)
    comment: Optional[str] = None

class ReviewResponse(ReviewBase):
    id: UUID
    provider_id: UUID
    client_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class ReviewListResponse(BaseModel):
    total: int
    average_rating: float
    page: int
    size: int
    items: List[ReviewResponse]
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from .availability import AvailabilityResponse

class ProviderBase(BaseModel):
    company_name: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class ProviderCreate(ProviderBase):
    pass

class ProviderUpdate(ProviderBase):
    pass

class ProviderResponse(ProviderBase):
    id: UUID
    user_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProviderDetailedResponse(ProviderResponse):
    average_rating: Optional[float]
    recent_reviews: List[dict]
    gallery: List[str]
    open_hours: List[AvailabilityResponse]

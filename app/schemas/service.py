from pydantic import BaseModel, HttpUrl
from typing import Optional
from uuid import UUID
from datetime import datetime

class ServiceBase(BaseModel):
    name: str
    category: str
    price: str
    duration: str
    description: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    popular: Optional[bool] = False

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    popular: Optional[bool] = None

class ServiceResponse(ServiceBase):
    id: UUID
    provider_id: UUID
    rating: float
    reviews_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
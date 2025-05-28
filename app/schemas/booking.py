from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
import enum

class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class BookingCreate(BaseModel):
    service_id: UUID
    start_datetime: datetime
    end_datetime: datetime

class BookingResponse(BaseModel):
    id: UUID
    service_id: UUID
    provider_id: UUID
    client_id: UUID
    start_datetime: datetime
    end_datetime: datetime
    status: BookingStatus

    class Config:
        from_attributes = True
from pydantic import BaseModel
from datetime import time
from uuid import UUID
import enum

class DayOfWeek(enum.IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

class AvailabilityBase(BaseModel):
    day_of_week: DayOfWeek
    start_time: time
    end_time: time

class AvailabilityCreate(AvailabilityBase):
    pass

class AvailabilityResponse(AvailabilityBase):
    id: UUID
    provider_id: UUID

    class Config:
        from_attributes = True
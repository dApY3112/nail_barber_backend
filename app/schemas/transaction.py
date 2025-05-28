from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
import enum

class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"

class TransactionCreate(BaseModel):
    booking_id: UUID
    amount: float = Field(..., gt=0)
    currency: str = "USD"
    payment_method: str

class TransactionResponse(TransactionCreate):
    id: UUID
    client_id: UUID
    status: TransactionStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
# app/models/rating.py
import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class Rating(Base):
    __tablename__ = "ratings"
    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id"), nullable=False)
    score      = Column(Integer,             nullable=False)   # 1..5
    created_at = Column(DateTime, default=datetime.utcnow)

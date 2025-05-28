import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Float, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("providers.id"), nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    price = Column(String(50), nullable=False)
    duration = Column(String(50), nullable=False)
    rating = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    popular = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

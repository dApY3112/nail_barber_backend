from typing import List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app.models.review import Review
from app.schemas.review import ReviewCreate
from app.models.provider import Provider

class CRUDReview:
    def create(self, db: Session, obj_in: ReviewCreate, client_id: str) -> Review:
        # Verify booking exists and ownership
        provider = db.get(Provider, obj_in.provider_id)
        if not provider:
            raise HTTPException(404, "Provider not found")
        # Create review
        db_obj = Review(
            provider_id=obj_in.provider_id,
            client_id=client_id,
            rating=obj_in.rating,
            comment=obj_in.comment
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_paginated_for_provider(
        self,
        db: Session,
        provider_id: str,
        skip: int = 0,
        limit: int = 20
    ) -> List[Review]:
        return (
            db.query(Review)
            .filter(Review.provider_id == provider_id)
            .order_by(Review.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_and_average_for_provider(self, db: Session, provider_id: str) -> Tuple[int, float]:
        result = db.query(
            func.count(Review.id).label('count'),
            func.coalesce(func.avg(Review.rating), 0).label('avg')
        ).filter(Review.provider_id == provider_id).one()
        return result.count, float(result.avg)

    def get_by_client(self, db: Session, client_id: str) -> List[Review]:
        return (
            db.query(Review)
            .filter(Review.client_id == client_id)
            .order_by(Review.created_at.desc())
            .all()
        )

crud_review = CRUDReview()
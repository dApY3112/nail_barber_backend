from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.review import ReviewCreate, ReviewResponse, ReviewListResponse
from app.crud.crud_review import crud_review
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_review.create(db, obj_in=review_in, client_id=str(current_user.id))

@router.get("/provider/{provider_id}", response_model=ReviewListResponse)
def list_reviews_for_provider(
    provider_id: str,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * size
    total, avg = crud_review.count_and_average_for_provider(db, provider_id=provider_id)
    items = crud_review.get_paginated_for_provider(db, provider_id=provider_id, skip=skip, limit=size)
    return ReviewListResponse(total=total, average_rating=round(avg, 2), items=items)

@router.get("/client/me", response_model=List[ReviewResponse])
def list_reviews_for_client(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_review.get_by_client(db, client_id=str(current_user.id))
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.availability import AvailabilityCreate, AvailabilityResponse
from app.crud.crud_availability import crud_availability
from app.crud.crud_provider import crud_provider
from app.models.user import User

router = APIRouter()

@router.post("/me", response_model=AvailabilityResponse, status_code=status.HTTP_201_CREATED)
def create_availability(
    obj_in: AvailabilityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    provider = crud_provider.get_by_user(db, user_id=str(current_user.id))
    if not provider:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a provider")
    return crud_availability.create(db, obj_in=obj_in, provider_id=str(provider.id))

@router.get("/me", response_model=List[AvailabilityResponse])
def list_availability(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    provider = crud_provider.get_by_user(db, user_id=str(current_user.id))
    if not provider:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a provider")
    return crud_availability.get_by_provider(db, provider_id=str(provider.id))

@router.delete("/me/{availability_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_availability(
    availability_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    provider = crud_provider.get_by_user(db, user_id=str(current_user.id))
    if not provider:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a provider")
    crud_availability.remove(db, availability_id=availability_id)
    return None
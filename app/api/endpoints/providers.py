from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.provider import (
    ProviderResponse,
    ProviderCreate,
    ProviderUpdate,
    ProviderDetailedResponse
)
from app.crud.crud_provider import crud_provider
from app.crud.crud_availability import crud_availability
from app.models.user import User
from app.schemas.user import UserRole
router = APIRouter()

@router.post("/", response_model=ProviderResponse, status_code=status.HTTP_201_CREATED)
def create_provider(
    provider_in: ProviderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1) kiểm tra đã có profile chưa
    existing = crud_provider.get_by_user(db, user_id=str(current_user.id))
    if existing:
        raise HTTPException(400, "Provider profile already exists")

    # 2) Tạo provider profile
    provider = crud_provider.create(db, obj_in=provider_in, user_id=str(current_user.id))

    # 3) Nâng role user thành provider
    current_user.role = UserRole.PROVIDER
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return provider

@router.get("/", response_model=List[ProviderResponse])
def list_providers(
    db: Session = Depends(get_db),
    page: int = 1,
    size: int = 20,
    city: Optional[str] = None,
    country: Optional[str] = None
):
    skip = (page - 1) * size
    return crud_provider.get_multi(db, skip=skip, limit=size, city=city, country=country)
@router.patch("/me", response_model=ProviderResponse)
def update_provider_me(
    provider_in: ProviderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    provider = crud_provider.get_by_user(db, user_id=str(current_user.id))
    if not provider:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider profile not found")
    return crud_provider.update(db, db_obj=provider, obj_in=provider_in)

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_provider_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    provider = crud_provider.get_by_user(db, user_id=str(current_user.id))
    if not provider:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider profile not found")
    crud_provider.remove(db, provider_id=str(provider.id))
    return None

@router.get("/me", response_model=ProviderResponse)
def read_provider_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    provider = crud_provider.get_by_user(db, user_id=str(current_user.id))
    if not provider:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider profile not found")
    return provider

@router.get("/{provider_id}", response_model=ProviderDetailedResponse)
def get_provider_detail(
    provider_id: UUID,
    db: Session = Depends(get_db)
):
    provider = crud_provider.get_detailed(db, provider_id)
    if not provider:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
    # fetch availability
    avail = crud_availability.get_by_provider(db, provider_id=provider_id)
    result = {**provider.__dict__, "average_rating": None, "recent_reviews": [], "gallery": [], "open_hours": avail}
    return ProviderDetailedResponse(**result)



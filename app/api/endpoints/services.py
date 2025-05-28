from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.service import ServiceCreate, ServiceResponse, ServiceUpdate
from app.crud.crud_service import crud_service
from app.crud.crud_provider import crud_provider
from app.models.user import User

router = APIRouter()

# Create a new service (only provider)
@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(
    service_in: ServiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    provider = crud_provider.get_by_user(db, user_id=str(current_user.id))
    if not provider:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a provider")
    return crud_service.create(db, obj_in=service_in, provider_id=str(provider.id))

# List own services
@router.get("/me", response_model=List[ServiceResponse])
def list_own_services(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100)
):
    provider = crud_provider.get_by_user(db, user_id=str(current_user.id))
    if not provider:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a provider")
    skip = (page - 1) * size
    return crud_service.get_by_provider(db, provider_id=str(provider.id), skip=skip, limit=size)

# Update own service
@router.patch("/me/{service_id}", response_model=ServiceResponse)
def update_service(
    service_id: str,
    service_in: ServiceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    provider = crud_provider.get_by_user(db, user_id=str(current_user.id))
    if not provider:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a provider")
    service = crud_service.get(db, service_id)
    if not service or str(service.provider_id) != str(provider.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return crud_service.update(db, db_obj=service, obj_in=service_in)

# Delete own service
@router.delete("/me/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(
    service_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    provider = crud_provider.get_by_user(db, user_id=str(current_user.id))
    if not provider:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a provider")
    service = crud_service.get(db, service_id)
    if not service or str(service.provider_id) != str(provider.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    crud_service.remove(db, service_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
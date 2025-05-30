from typing import List, Optional, Tuple
from fastapi import APIRouter, Depends, HTTPException, status, Query, Response, Path, Body
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.crud.crud_service import crud_service
from app.crud.crud_provider import crud_provider
from app.models.user import User
from app.schemas.service import (
    ServiceCreate,
    ServiceResponse,
    ServiceUpdate,
    ServiceList,
)
from app.schemas.category import CategoryResponse
from app.schemas.rating import RatingCreate
from app.models.service import Service
from app.schemas.service import ServiceResponse

router = APIRouter()


# Public endpoint – list all services with pagination / filtering / search
@router.get(
    "/",
    response_model=ServiceList,
    summary="Public: list services with pagination, category, search & provider filter",
)
def list_services(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    provider_id: Optional[str] = Query(None),    # thêm param provider_id
):
    skip = (page - 1) * size

    # build filters dict
    filters: dict[str, Optional[str]] = {}
    if category:
        filters["category"] = category
    if search:
        filters["search"] = search
    if provider_id:
        filters["provider_id"] = provider_id

    # gọi get_multi với filters đã có provider_id
    total, items = crud_service.get_multi(
        db,
        skip=skip,
        limit=size,
        filters=filters,
    )
    return {"total": total, "items": items}


@router.get(
    "/categories",
    response_model=List[CategoryResponse],   # hoặc List[str] nếu bạn không dùng schema
    summary="List all distinct service categories"
)
def list_service_categories(
    db: Session = Depends(get_db),
):
    cats = crud_service.get_categories(db)
    # nếu dùng List[str]:
    # return cats
    # nếu dùng List[CategoryResponse]:
    return [{"id": c, "name": c} for c in cats]
# Create a new service (only provider)
@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(
    service_in: ServiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    provider = crud_provider.get_by_user(db, user_id=str(current_user.id))
    if not provider:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a provider")
    return crud_service.create(db, obj_in=service_in, provider_id=str(provider.id))


# List own services (provider only)
@router.get("/me", response_model=List[ServiceResponse])
def list_own_services(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    provider = crud_provider.get_by_user(db, user_id=str(current_user.id))
    if not provider:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a provider")
    skip = (page - 1) * size
    return crud_service.get_by_provider(db, provider_id=str(provider.id), skip=skip, limit=size)


# Update own service (provider only)
@router.patch("/me/{service_id}", response_model=ServiceResponse)
def update_service(
    service_id: str,
    service_in: ServiceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    provider = crud_provider.get_by_user(db, user_id=str(current_user.id))
    if not provider:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a provider")
    service = crud_service.get(db, service_id)
    if not service or str(service.provider_id) != str(provider.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return crud_service.update(db, db_obj=service, obj_in=service_in)


# Delete own service (provider only)
@router.delete("/me/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(
    service_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    provider = crud_provider.get_by_user(db, user_id=str(current_user.id))
    if not provider:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a provider")
    service = crud_service.get(db, service_id)
    if not service or str(service.provider_id) != str(provider.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    crud_service.remove(db, service_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
@router.post(
    "/{service_id}/rating",
    status_code=status.HTTP_201_CREATED,
    summary="Public: submit a rating (1–5) for a service",
)
def rate_service(
    service_id: str = Path(..., description="ID of the service to rate"),
    payload: RatingCreate = Body(...),
    db: Session = Depends(get_db),
):
    # 1. kiểm tra service tồn tại
    svc = crud_service.get(db, service_id)
    if not svc:
        raise HTTPException(status_code=404, detail="Service not found")
    # 2. thêm rating và cập nhật average + count
    crud_service.add_rating(db, service_id, payload.score)
    # 3. trả về giá trị mới
    return {
        "rating": svc.rating,
        "reviews_count": svc.reviews_count
    }
@router.get(
    "/{service_id}",
    response_model=ServiceResponse,
    summary="Get a single service by ID"
)
def get_service(
    service_id: str,
    db: Session = Depends(get_db)
):
    svc = db.get(Service, service_id)
    if not svc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    return svc
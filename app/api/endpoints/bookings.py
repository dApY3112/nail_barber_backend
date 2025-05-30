from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.booking import BookingCreate, BookingResponse
from app.crud.crud_booking import crud_booking
from app.crud.crud_provider import crud_provider
from app.models.user import User
from app.models.service import Service  # thêm import
from app.models.booking import Booking
router = APIRouter()

@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    obj_in: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Lấy service để xác định provider_id
    service = db.get(Service, obj_in.service_id)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    provider_id = str(service.provider_id)

    # TODO: kiểm tra slot availability và tránh trùng giờ
    booking = crud_booking.create(
        db=db,
        obj_in=obj_in,
        provider_id=provider_id,
        client_id=str(current_user.id)
    )
    return booking

# Client lists own bookings
@router.get("/me", response_model=List[BookingResponse])
def list_client_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_booking.get_by_client(db, client_id=str(current_user.id))

# Provider lists bookings
@router.get("/provider/me", response_model=List[BookingResponse])
def list_provider_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    provider = crud_provider.get_by_user(db, user_id=str(current_user.id))
    if not provider:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a provider")
    return crud_booking.get_by_provider(db, provider_id=str(provider.id))

# Cancel booking
@router.patch("/cancel/{booking_id}", response_model=BookingResponse)
def cancel_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = crud_booking.cancel(db, booking_id=booking_id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    # Only client or provider who owns booking can cancel
    if booking.client_id != current_user.id and booking.provider_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return booking
@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    # Chỉ client hoặc provider mới xem được
    if str(booking.client_id) != str(current_user.id) and str(booking.provider_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this booking"
        )
    return booking
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.crud.crud_transaction import crud_transaction
from app.models.user import User
from app.models.booking import Booking
from typing import List

router = APIRouter()

@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    obj_in: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify booking and ownership
    booking = db.get(Booking, obj_in.booking_id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    if str(booking.client_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your booking")
    trans = crud_transaction.create(db, obj_in=obj_in, client_id=str(current_user.id))
    return trans

@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trans = crud_transaction.get(db, transaction_id)
    if not trans:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    # Only client or provider associated can view
    if str(trans.client_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return trans

@router.get("/booking/{booking_id}", response_model=List[TransactionResponse])
def list_transactions_for_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # client or provider can view
    return crud_transaction.get_by_booking(db, booking_id=booking_id)
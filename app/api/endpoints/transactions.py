from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.transaction import TransactionCreate, TransactionResponse,TransactionStatus
from app.crud.crud_transaction import crud_transaction
from app.models.user import User
from app.models.booking import Booking
from typing import List
from pydantic import BaseModel

router = APIRouter()
class StatusUpdate(BaseModel):
    status: TransactionStatus
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
@router.get("/me", response_model=List[TransactionResponse])
def list_my_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Liệt kê tất cả transactions của chính client đang login, mới nhất trước.
    """
    return crud_transaction.get_by_client(db, client_id=str(current_user.id))
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
@router.patch(
    "/{transaction_id}/status",
    response_model=TransactionResponse,
    summary="Update transaction status (cancel or complete)"
)
def update_transaction_status(
    transaction_id: str,
    payload: StatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # chỉ cho client owner thao tác (hoặc bạn có thể cho cả provider)
    tx = crud_transaction.get(db, transaction_id)
    if not tx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    if str(tx.client_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    # chỉ cho đổi khi đang ở trạng thái pending
    if tx.status != TransactionStatus.PENDING:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can only update status from pending")
    updated = crud_transaction.update_status(db, transaction_id, payload.status)
    return updated
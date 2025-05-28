from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.transaction import Transaction, TransactionStatus
from app.schemas.transaction import TransactionCreate

class CRUDTransaction:
    def create(
        self,
        db: Session,
        obj_in: TransactionCreate,
        client_id: str
    ) -> Transaction:
        # Create pending transaction record
        db_obj = Transaction(
            booking_id=obj_in.booking_id,
            client_id=client_id,
            amount=obj_in.amount,
            currency=obj_in.currency,
            payment_method=obj_in.payment_method,
            status=TransactionStatus.PENDING
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        # TODO: integrate with payment gateway and update status
        return db_obj

    def get(
        self,
        db: Session,
        transaction_id: str
    ) -> Optional[Transaction]:
        return db.get(Transaction, transaction_id)

    def get_by_booking(
        self,
        db: Session,
        booking_id: str
    ) -> List[Transaction]:
        return (
            db.query(Transaction)
            .filter(Transaction.booking_id == booking_id)
            .all()
        )

    def update_status(
        self,
        db: Session,
        transaction_id: str,
        status: TransactionStatus
    ) -> Transaction:
        db_obj = db.get(Transaction, transaction_id)
        db_obj.status = status
        db.commit()
        db.refresh(db_obj)
        return db_obj

crud_transaction = CRUDTransaction()

from typing import List
from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.schemas.booking import BookingCreate

class CRUDBooking:
    def create(self, db: Session, obj_in: BookingCreate, provider_id: str, client_id: str) -> Booking:
        db_obj = Booking(
            service_id=obj_in.service_id,
            provider_id=provider_id,
            client_id=client_id,
            start_datetime=obj_in.start_datetime,
            end_datetime=obj_in.end_datetime
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_client(self, db: Session, client_id: str) -> List[Booking]:
        return db.query(Booking).filter(Booking.client_id == client_id).all()

    def get_by_provider(self, db: Session, provider_id: str) -> List[Booking]:
        return db.query(Booking).filter(Booking.provider_id == provider_id).all()

    def cancel(self, db: Session, booking_id: str) -> Booking:
        db_obj = db.get(Booking, booking_id)
        if db_obj:
            db_obj.status = 'cancelled'
            db.commit()
            db.refresh(db_obj)
        return db_obj

crud_booking = CRUDBooking()
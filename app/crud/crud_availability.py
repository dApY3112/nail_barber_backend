from typing import List
from sqlalchemy.orm import Session
from app.models.availability import ProviderAvailability
from app.schemas.availability import AvailabilityCreate

class CRUDAvailability:
    def create(self, db: Session, obj_in: AvailabilityCreate, provider_id: str) -> ProviderAvailability:
        db_obj = ProviderAvailability(
            provider_id=provider_id,
            day_of_week=obj_in.day_of_week,
            start_time=obj_in.start_time,
            end_time=obj_in.end_time
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_provider(self, db: Session, provider_id: str) -> List[ProviderAvailability]:
        return db.query(ProviderAvailability).filter(ProviderAvailability.provider_id == provider_id).all()

    def remove(self, db: Session, availability_id: str) -> None:
        obj = db.get(ProviderAvailability, availability_id)
        if obj:
            db.delete(obj)
            db.commit()

crud_availability = CRUDAvailability()
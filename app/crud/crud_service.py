from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate

class CRUDService:
    def create(self, db: Session, obj_in: ServiceCreate, provider_id: str) -> Service:
        db_obj = Service(
            provider_id=provider_id,
            name=obj_in.name,
            category=obj_in.category,
            price=obj_in.price,
            duration=obj_in.duration,
            description=obj_in.description,
            image_url=str(obj_in.image_url) if obj_in.image_url else None,
            popular=obj_in.popular or False
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, service_id: str) -> Optional[Service]:
        return db.get(Service, service_id)

    def get_by_provider(
        self, db: Session, provider_id: str, skip: int = 0, limit: int = 100
    ) -> List[Service]:
        return (
            db.query(Service)
            .filter(Service.provider_id == provider_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
        self, db: Session, db_obj: Service, obj_in: ServiceUpdate
    ) -> Service:
        update_data = obj_in.dict(exclude_unset=True)
        if "image_url" in update_data and update_data["image_url"] is not None:
            update_data["image_url"] = str(update_data["image_url"])
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(
        self, db: Session, service_id: str
    ) -> None:
        obj = db.get(Service, service_id)
        if obj:
            db.delete(obj)
            db.commit()

crud_service = CRUDService()

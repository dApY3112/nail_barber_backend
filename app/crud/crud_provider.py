from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.provider import Provider
from app.schemas.provider import ProviderCreate, ProviderUpdate

class CRUDProvider:
    def create(self, db: Session, obj_in: ProviderCreate, user_id: str) -> Provider:
        db_obj = Provider(
            user_id=user_id,
            company_name=obj_in.company_name,
            description=obj_in.description,
            city=obj_in.city,
            country=obj_in.country
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, provider_id: str) -> Optional[Provider]:
        return db.get(Provider, provider_id)

    def get_by_user(self, db: Session, user_id: str) -> Optional[Provider]:
        return db.query(Provider).filter(Provider.user_id == user_id).first()

    def get_multi(self,
                db: Session,
                skip: int = 0,
                limit: int = 20,
                city: Optional[str] = None,
                country: Optional[str] = None
                ) -> List[Provider]:
        query = db.query(Provider)
        if city:
            query = query.filter(Provider.city == city)
        if country:
            query = query.filter(Provider.country == country)
        query = query.offset(skip).limit(limit)
        return query.all()

    def get_detailed(self, db: Session, provider_id: str) -> Optional[Provider]:
        return self.get(db, provider_id)

    def update(self, db: Session, db_obj: Provider, obj_in: ProviderUpdate) -> Provider:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, provider_id: str) -> None:
        obj = db.get(Provider, provider_id)
        if obj:
            db.delete(obj)
            db.commit()

crud_provider = CRUDProvider()
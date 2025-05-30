from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate
from app.models.rating import Rating
from sqlalchemy import or_, distinct, func
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
    def get_multi(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: dict[str, Optional[str]] = None
    ) -> Tuple[int, List[Service]]:
        query = db.query(Service)
        if filters:
            if filters.get("provider_id"):
                query = query.filter(Service.provider_id == filters["provider_id"])
            if filters.get("category"):
                query = query.filter(Service.category == filters["category"])
            if filters.get("search"):
                term = f"%{filters['search']}%"
                query = query.filter(
                    or_(
                        Service.name.ilike(term),
                        Service.description.ilike(term)
                    )
                )
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return total, items
    def get_categories(self, db: Session) -> List[str]:
        """
        Trả về danh sách các category (string) duy nhất trong bảng services
        """
        rows = db.query(distinct(Service.category)).all()
        # rows có dạng [( 'hair', ), ( 'nails', ), ...]
        return [r[0] for r in rows]  
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

    def remove(self, db: Session, service_id: str) -> None:
        # Xóa tất cả ratings liên quan
        db.query(Rating).filter(Rating.service_id == service_id).delete()
        obj = db.get(Service, service_id)
        if obj:
            db.delete(obj)
            db.commit()
    def add_rating(self, db: Session, service_id: str, score: int) -> Rating:
        new = Rating(service_id=service_id, score=score)
        db.add(new)
        db.commit()
        # update aggregate trên Service
        agg = db.query(
            func.avg(Rating.score), func.count(Rating.id)
        ).filter(Rating.service_id == service_id).one()
        avg_score, cnt = float(agg[0]), agg[1]
        svc = db.get(Service, service_id)
        svc.rating = avg_score
        svc.reviews_count = cnt
        db.commit()
        return new

crud_service = CRUDService()

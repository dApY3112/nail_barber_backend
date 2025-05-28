from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password

class CRUDUser:
    def create(self, db: Session, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            password_hash=hash_password(obj_in.password),
            role=obj_in.role
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def get(self, db: Session, user_id: str) -> User | None:
        return db.get(User, user_id)

    def update(self, db: Session, db_obj: User, obj_in: UserUpdate) -> User:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def change_password(self, db: Session, db_obj: User, new_password: str) -> User:
        db_obj.password_hash = hash_password(new_password)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, user_id: str) -> None:
        obj = db.get(User, user_id)
        if obj:
            db.delete(obj)
            db.commit()

crud_user = CRUDUser()
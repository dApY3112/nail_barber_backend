from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.user import UserCreate, UserResponse, UserUpdate, PasswordChange
from app.crud.crud_user import crud_user
from app.core.security import verify_password

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    existing = crud_user.get_by_email(db, email=user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    user = crud_user.create(db, obj_in=user_in)
    return user

@router.get("/me", response_model=UserResponse)
def read_users_me(
    current_user = Depends(get_current_user)
):
    return current_user

@router.patch("/me", response_model=UserResponse)
def update_users_me(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user = crud_user.update(db, db_obj=current_user, obj_in=user_in)
    return user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_users_me(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    crud_user.remove(db, user_id=str(current_user.id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    password_data: PasswordChange,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect current password")
    crud_user.change_password(db, db_obj=current_user, new_password=password_data.new_password)
    return {"msg": "Password changed successfully"}
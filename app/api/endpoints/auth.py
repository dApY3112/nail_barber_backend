from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.api.deps import get_db
from app.crud.crud_user import crud_user
from app.core.security import verify_password, create_access_token, create_password_reset_token, verify_password_reset_token
from app.core.config import settings
from app.schemas.token import Token
from app.schemas.user import PasswordResetRequest, PasswordReset

router = APIRouter()

@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = crud_user.get_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forgot-password")
def forgot_password(request: PasswordResetRequest, db: Session = Depends(get_db)):
    user = crud_user.get_by_email(db, email=request.email)
    if user:
        reset_token = create_password_reset_token({"sub": str(user.id)})
        # TODO: Integrate email service to send reset_token to user.email
        print(f"Password reset token for {user.email}: {reset_token}")
    return {"msg": "If an account with that email exists, you will receive a password reset email."}

@router.post("/reset-password")
def reset_password(request: PasswordReset, db: Session = Depends(get_db)):
    try:
        user_id = verify_password_reset_token(request.token)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
    user = crud_user.get(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    crud_user.change_password(db, db_obj=user, new_password=request.new_password)
    return {"msg": "Password reset successfully."}

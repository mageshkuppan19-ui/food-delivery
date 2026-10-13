from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import create_access_token, create_refresh_token, decode_token, verify_password
from app.crud.user import create_user, get_user_by_email
from app.database.session import get_db
from app.models.user import RefreshToken
from app.schemas.user import (
    ForgotPasswordRequest,
    LoginRequest,
    RefreshRequest,
    ResetPasswordRequest,
    TokenResponse,
    UserCreate,
    UserOut,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, payload)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(str(user.id), {"role": user.role})
    refresh_token = create_refresh_token(str(user.id))

    db.add(
        RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=datetime.utcnow() + timedelta(days=7),
        )
    )
    db.commit()
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    try:
        data = decode_token(payload.refresh_token)
        if data.get("type") != "refresh":
            raise JWTError()
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    stored = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == payload.refresh_token, RefreshToken.revoked.is_(False))
        .first()
    )
    if not stored:
        raise HTTPException(status_code=401, detail="Refresh token not recognized")

    new_access = create_access_token(data["sub"])
    return TokenResponse(access_token=new_access, refresh_token=payload.refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(payload: RefreshRequest, db: Session = Depends(get_db)):
    stored = db.query(RefreshToken).filter(RefreshToken.token == payload.refresh_token).first()
    if stored:
        stored.revoked = True
        db.commit()
    return None


@router.post("/forgot-password", status_code=status.HTTP_202_ACCEPTED)
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    # In production: generate a reset token, email it via the notification service.
    user = get_user_by_email(db, payload.email)
    if user:
        pass  # trigger notification service here
    return {"message": "If that email exists, a reset link has been sent."}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    # In production: validate the reset token and update the user's password.
    return {"message": "Password has been reset."}


@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    # In production: validate the emailed verification token, set user.is_verified = True.
    return {"message": "Email verified."}

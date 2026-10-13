from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.user import delete_user, get_user, list_users
from app.database.session import get_db
from app.middleware.auth import get_current_user, require_role
from app.models.user import RoleEnum
from app.schemas.user import UserOut

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[UserOut])
def get_users(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    _admin=Depends(require_role(RoleEnum.ADMIN)),
):
    return list_users(db, skip, limit)


@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=204)
def remove_user(
    user_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(require_role(RoleEnum.ADMIN)),
):
    delete_user(db, user_id)
    return None

from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from techconnect_classes_api.api.limiter import limiter
from techconnect_classes_api.core.security import get_password_hash
from techconnect_classes_api.crud.user import user_crud
from techconnect_classes_api.database.db import get_db
from techconnect_classes_api.schemas.auth import UserSignUp
from techconnect_classes_api.schemas.user import UserInDB

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("1/second")
def sign_up_user(
    request: Request, user_data: UserSignUp, db: Annotated[Session, Depends(get_db)]
) -> dict[str, str]:
    """Endpoint to sign up for an account with username and password.

    Parameters:
        user_data (UserSignUp): Request body containing username and password.
        db (Session): The database session.
    Returns:
        dict[str, str]: A dictionary containing the username created.
    """
    user = user_crud.get_user(db, user_data.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"'{user_data.username}' already registered",
        )
    user_in = UserInDB(
        username=user_data.username,
        hashed_password=get_password_hash(user_data.password),
    )
    user_crud.insert(db, obj_in=user_in)
    return {"username": user_data.username}


# @router.get("/me", response_model=...)
# @limiter.limit("1/second")
# def get_user_info():
#     raise


# @router.post("/me", response_model=...)
# @limiter.limit("1/second")
# def create_user_info():
#     raise


# @router.patch("/me", response_model=...)
# @limiter.limit("1/second")
# def update_user_info():
#     raise


# @router.delete("/me", response_model=...)
# @limiter.limit("1/second")
# def delete_user_info():
#     raise

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from techconnect_classes_api.api.limiter import limiter
from techconnect_classes_api.core.config import settings
from techconnect_classes_api.core.security import create_access_token
from techconnect_classes_api.crud.user import user_crud
from techconnect_classes_api.database import get_db
from techconnect_classes_api.schemas.auth import Token

router = APIRouter()


@router.post("/token", status_code=status.HTTP_200_OK)
@limiter.limit("1/second")
def login_for_access_token(
    db: Annotated[Session, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """Endpoint to aquire access token using the provided username and password to authenticate user.

    Parameters:
        db (Session): The database session.
        form_data (OAuth2PasswordRequestForm): The form data
        containing the username and password.
    Returns:
        Token: A Token object containing the access token and token type.
    """
    user = user_crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

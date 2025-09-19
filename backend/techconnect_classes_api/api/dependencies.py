from typing import Annotated

import jwt
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from techconnect_classes_api.core.config import settings
from techconnect_classes_api.core.exceptions import credentials_exception
from techconnect_classes_api.database import get_db
from techconnect_classes_api.models import User
from techconnect_classes_api.schemas.auth import TokenPayload
from techconnect_classes_api.crud.user import user_crud

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_token(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenPayload:
    try:
        """Retrive jwt token from payload"""
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception()
    except ExpiredSignatureError:
        raise credentials_exception(detail="Token has expired")
    except PyJWTError:
        raise credentials_exception()
    return TokenPayload(sub=sub)


def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[TokenPayload, Depends(get_token)],
) -> User:
    try:
        user_id = int(token.sub)
    except (ValueError, TypeError):
        raise credentials_exception(detail="Invalid token")
    user = user_crud.get(db, User.id == user_id)
    if user is None:
        raise credentials_exception()
    return user


def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.is_active:
        raise credentials_exception(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user

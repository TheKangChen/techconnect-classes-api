from sqlalchemy.orm import Session

from techconnect_classes_api.core.security import verify_password
from techconnect_classes_api.models import User

from .base import CRUDBase


class UserCRUD(CRUDBase):
    def get_user(self, db: Session, username: str) -> User | None:
        return self.get(db, self.model.username == username)

    def authenticate_user(
        self, db: Session, username: str, password: str
    ) -> User | None:
        """Authenticate user on login"""
        user = self.get_user(db, username)
        if not user:
            return None
        if not verify_password(password, str(user.hashed_password)):
            return None
        return user

    @staticmethod
    def is_active_user(user: User) -> bool:
        return user.is_active

    def deactivate_user(self, db: Session, user: User) -> User:
        user.is_active = False
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


user_crud = UserCRUD(model=User)

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    is_active: bool = True


class UserCreate(UserBase):
    """..."""
    password: str


class UserInDB(UserBase):
    hashed_password: str

from uuid import UUID, uuid4
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


from src.auth.security import verify_password
from src.auth.security import get_password_hash
from src.auth.security import generate_salt
from src.marketplace.schemas.basket import Basket


class UserBase(BaseModel):
    login: str = Field(..., max_length=40, min_length=5)
    email: EmailStr = Field(..., max_length=255)


class UserCreate(UserBase):
    password: str = Field(..., min_length=5, max_length=50)


class UserLogin(BaseModel):
    login: Optional[str] = Field(default=None, max_length=40, min_length=5)
    email: Optional[EmailStr] = Field(default=None, max_length=255)
    password: str = Field(..., min_length=5, max_length=50)


class UserSchema(UserBase):
    id: UUID = Field(default_factory=uuid4)
    basket: list[Basket] = []
    hashed_password: str = Field(...)
    salt: str = Field(...)

    class Config:
        from_attributes = True


class UserDB(UserBase):
    id: UUID = Field(default_factory=uuid4)
    is_admin: bool = Field(default=False)
    hashed_password: str = Field(default="")
    salt: str = Field(default="")

    def check_password(self, password: str):
        return verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str):
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)


class UserResponse(UserBase):
    id: UUID = Field(...)
    is_admin: bool = Field(default=False)
    token: str = Field(...)  # access token

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    login: str | None = Field(default=None, max_length=40, min_length=5)
    password: str | None = Field(default=None, max_length=50, min_length=5)


class TokenPayload(BaseModel):
    login: str = Field(..., max_length=40, min_length=5)
    is_admin: bool = Field(default=False)

from fastapi import HTTPException, status
from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import UserCreate, UserDB, UserSchema, UserLogin
from src.auth.models import User
from src.auth.security import verify_password


async def create_user(user: UserCreate, session: AsyncSession) -> UserDB:

    new_user = UserDB(**user.model_dump())
    new_user.change_password(user.password)

    user_model = User(**UserSchema(**new_user.model_dump()).model_dump())
    await user_model.save(session)

    return new_user


async def check_user_in_login(user: UserLogin, session: AsyncSession) -> Union[User, HTTPException]:

    if user.email:
        exist_user = await User.check_email(user.email, session)
        if not exist_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User with current email not found!")

    if user.login:
        exist_user = await User.check_login(user.login, session)
        if not exist_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User with current login not found!")

    if not user.email and not user.login:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Not correct input data!")

    if not verify_password(exist_user.salt + user.password, exist_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Current password incorrect")
    return exist_user

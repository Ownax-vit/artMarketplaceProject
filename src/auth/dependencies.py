from fastapi import Cookie, HTTPException
from fastapi import Depends, status
from fastapi import Header
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from src.auth.models import User
from src.auth.schemas import TokenPayload
from src.config import settings
from src.database import get_async_session


def _get_authorization_token(authorization: str = Header(...)):
    try:
        token_prefix, token = authorization.split(" ")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid authorization token name",
        )
    if token_prefix != settings.jwt_token_prefix:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization type token ",
        )
    return token


def _get_authorization_token_refresh(refresh_token: str = Cookie(...)):
    token = _get_authorization_token(refresh_token)
    return token


async def _get_current_user(
    session: AsyncSession = Depends(get_async_session),
    token: str = Depends(_get_authorization_token),
) -> User:
    try:
        payload = jwt.decode(token, settings.secret_key.get_secret_value(),
                             algorithms=settings.algorithm_jwt)
        token_data = TokenPayload(**payload)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials"
        )

    user = await User.check_login(token_data.login, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


async def get_current_user_refresh(
    session: AsyncSession = Depends(get_async_session),
    token: str = Depends(_get_authorization_token_refresh),
) -> User:
    """ token from cookies """
    user = await _get_current_user(session, token)
    return user


def _get_authorization_token_optional(authorization: str = Header(None)):
    if authorization:
        return _get_authorization_token(authorization)
    return


async def _get_current_user_optional(
    session: AsyncSession = Depends(get_async_session),
    token: str = Depends(_get_authorization_token_optional),
) -> User | None:
    if token:
        return await _get_current_user(session, token)
    return None


def get_current_user_authorizer(*, required: bool = True):
    if required:
        return _get_current_user
    else:
        return _get_current_user_optional

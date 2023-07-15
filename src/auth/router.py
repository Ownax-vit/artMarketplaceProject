from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from fastapi import status
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.utils import set_refresh_token, clear_refresh_token
from src.database import get_async_session
from src.auth.schemas import UserCreate, UserResponse, TokenPayload, UserLogin
from src.auth.models import User
from src.auth.service import create_user, check_user_in_login
from src.auth.security import create_access_token
from src.auth.dependencies import get_current_user_refresh

router = APIRouter(tags=["auth"])


@router.post("/sign-up",  tags=["auth"], response_model=UserResponse,
             status_code=status.HTTP_201_CREATED)
async def registration(response: Response,
                       user: UserCreate,
                       session: AsyncSession = Depends(get_async_session)):
    exist_user = await User.check_login(user.login, session)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Current name is not available")

    exist_user = await User.check_email(user.email, session)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Current email is not available")

    token_payload = TokenPayload(login=user.login)
    token = create_access_token(data=token_payload.model_dump())
    try:
        resp_user = await create_user(user, session)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Error while create user!")

    set_refresh_token(response, resp_user.model_dump())

    return UserResponse(**resp_user.model_dump(), token=token)


@router.post("/sign-in", tags=["auth"], status_code=status.HTTP_200_OK,
             response_model=UserResponse)
async def login(response: Response,
                user: UserLogin,
                session: AsyncSession = Depends(get_async_session)):

    exist_user = await check_user_in_login(user, session)

    token_payload = TokenPayload(login=exist_user.login)
    token = create_access_token(data=token_payload.model_dump())
    set_refresh_token(response, {"login": exist_user.login})

    return UserResponse(email=exist_user.email, id=exist_user.id,
                        token=token, is_admin=exist_user.is_admin,
                        login=exist_user.login)


@router.post("/refresh", response_model=UserResponse, tags=["auth"],
             status_code=status.HTTP_201_CREATED)
async def refresh_token(response: Response, user: User = Depends(get_current_user_refresh),
                        session: AsyncSession = Depends(get_async_session)):
    exist_user = await User.check_login(user.login, session)
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Current user not found!")

    token_payload = TokenPayload(login=exist_user.login)
    token = create_access_token(data=token_payload.model_dump())
    set_refresh_token(response, {"login": exist_user.login})

    return UserResponse(email=exist_user.email, id=exist_user.id,
                        token=token, is_admin=exist_user.is_admin,
                        login=exist_user.login)


@router.post("/sign-out", tags=["auth"], status_code=status.HTTP_200_OK)
async def logout(response: Response,
                 user: User = Depends(get_current_user_refresh)):
    clear_refresh_token(response)

from fastapi import Response

from src.auth.schemas import TokenPayload, UserResponse
from src.auth.security import create_refresh_token
from src.config import settings


def set_refresh_token(response: Response, data: dict) -> None:
    token_payload = TokenPayload(**data)
    refresh_token = create_refresh_token(data=token_payload.model_dump())
    response.set_cookie(
        key=settings.jwt_refresh_token_name,
        value=f"{settings.jwt_token_prefix} {refresh_token}",
        httponly=True,
    )


def clear_refresh_token(response: Response):
    response.delete_cookie(settings.jwt_refresh_token_name)
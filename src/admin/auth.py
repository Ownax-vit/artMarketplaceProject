from typing import Optional

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from fastapi import HTTPException
from pydantic import ValidationError

from src.auth.security import create_access_token
from src.auth.service import check_user_in_login
from src.auth.schemas import UserLogin, TokenPayload
from src.database import async_session_maker


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        login, password = form["username"], form["password"]
        try:
            async with async_session_maker() as session:
                user = await check_user_in_login(UserLogin(login=login, password=password), session)
                if not user.is_admin:
                    return False
        except ValidationError:
            return False
        except HTTPException:
            return False

        token_payload = TokenPayload(login=login)
        token = create_access_token(data=token_payload.model_dump())
        request.session.update({"token": token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

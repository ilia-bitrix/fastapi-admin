from aioredis import Redis
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request

from app.other_apps.fastapi_admin import constants
from app.other_apps.fastapi_admin.providers.base_login import UsernamePasswordProvider
from app.other_apps.fastapi_admin.utils import hash_password


class LoginProviderAdmin(UsernamePasswordProvider):
    async def create_user(self, email: str, password: str):
        obj = await self.admin_model.create(
            email=email,
            password=hash_password(password),
            is_super=True,
            is_active=True,
        )
        return obj

    async def authenticate(
            self,
            request: Request,
            call_next: RequestResponseEndpoint,
    ):
        """ check is superuser  """
        redis = request.app.redis  # type:Redis
        token = request.cookies.get(self.access_token)
        path = request.scope["path"]  # type:str
        if token:
            token_key = constants.LOGIN_USER.format(token=token)
            admin_email = await redis.get(token_key)
            admin = await self.admin_model.get_or_none(email = admin_email)
        else:
            admin = None

        request.state.admin = admin

        #  Check user
        if path == self.login_path or path == '/init':
            """ 
                Redirect to login page 
            """
            response = await call_next(request)
            return response
        elif admin == None:
            return self.redirect_init(request)
        elif not admin.is_super or not admin.is_active:
            return self.redirect_init(request)
        response = await call_next(request)
        return response



from aioredis import Redis
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

from fastapi_admin import constants
from .login import UsernamePasswordProvider


class LoginProviderAdmin(UsernamePasswordProvider):

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
            admin_id = await redis.get(token_key)
            admin = await self.admin_model.get_or_none(pk=admin_id)
        else:
            admin = None

        request.state.admin = admin

        if path != self.login_path and not admin:
            return RedirectResponse(url=request.app.admin_path, status_code=HTTP_303_SEE_OTHER)
        elif not admin.is_active:
            return RedirectResponse(url=request.app.admin_path, status_code=HTTP_303_SEE_OTHER)
        response = await call_next(request)
        return response




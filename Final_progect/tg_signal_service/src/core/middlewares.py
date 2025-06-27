from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from .utils import verify_auth_token


class VerifyAuthTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")
        if not_verify:=verify_auth_token(request):
            return not_verify
        response = await call_next(request)
        return response

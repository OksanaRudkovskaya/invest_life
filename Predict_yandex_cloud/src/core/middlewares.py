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

# class GetMetrics(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         start = time.time()
#         response = await call_next(request)
#         req_time = time.time() - start
#         app_name = request.app.title
#         app_metrics['request_time'].labels(
#             app_name=app_name,
#             req_url=request.url.path,
#             method=request.method,
#             http_status=response.status_code
#             ).observe(req_time)
#         return response
from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse

from settings import FASTAPI_TOKEN_HEADER, FASTAPI_VERIFY_TOKEN_MIDDLEWARE


def verify_auth_token(request: Request):
    if FASTAPI_VERIFY_TOKEN_MIDDLEWARE:
        return None

    auth_header = request.headers.get("Authorization")
    if auth_header != FASTAPI_TOKEN_HEADER:
        return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authentication token"}
            )
    return None
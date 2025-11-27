from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse

from settings import EXPECTED_TOKEN


def verify_auth_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header != EXPECTED_TOKEN:
        return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authentication token"}
            )
    return None
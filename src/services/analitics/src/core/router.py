from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse


router = APIRouter()

@router.get("/")
async def index(request: Request):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "Hello!"}
    )
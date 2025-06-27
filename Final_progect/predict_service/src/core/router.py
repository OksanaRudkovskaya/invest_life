from datetime import datetime

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse


router = APIRouter()

@router.get("/")
async def index(request: Request):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "Hello!"}
    )

lastTime = None
@router.get("/counters")
async def index(request: Request):
    global lastTime

    resp = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "startDttm": "2025-01-01 00:00:00.000",
            "lastDttm": lastTime,
            "curDttm": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            "counters": {
                "c1:true": 123,
                "c1:false": 12,
                "c2:true": 98,
                "c2:false": 36,
            }
        }
    )
    lastTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    return resp
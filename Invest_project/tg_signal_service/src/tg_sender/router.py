from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

from src.core.utils import verify_auth_token
from settings import TELEGRAM_CHAT_IDS


router = APIRouter()

class MessageModel(BaseModel):
    message: str
    chat_id: Optional[List[int]] = None


@router.post("/send_message_to_telegram")
async def send_message_to_telegram(message: MessageModel, request: Request, not_verified = Depends(verify_auth_token)):
    if not_verified:
        return not_verified

    chat_ids = message.chat_id
    if chat_ids is None:
        chat_ids = TELEGRAM_CHAT_IDS

    for chat_id in chat_ids:
        await request.app.bot.send_message(chat_id=chat_id, text=message.message)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Message sent successfully.",
    )

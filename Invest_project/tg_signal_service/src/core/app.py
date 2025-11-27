import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .middlewares import VerifyAuthTokenMiddleware
from .router import router as core_router

from src.tg_sender.router import router as tg_sender_router
from settings import FASTAPI_VERIFY_TOKEN_MIDDLEWARE

logger = logging.getLogger('uvicorn')


def create_app():
    app = FastAPI(
        title="ML Prediction Service",
        lifespan=lifespan
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    if FASTAPI_VERIFY_TOKEN_MIDDLEWARE:
        app.add_middleware(VerifyAuthTokenMiddleware)

    app.include_router(core_router)
    app.include_router(tg_sender_router, prefix="/api/v1")

    return app


async def lifespan(app: FastAPI):
    from aiogram import Bot
    from settings import TELEGRAM_BOT_TOKEN

    app.bot = Bot(token=TELEGRAM_BOT_TOKEN)
    logger.info('Telegram Bot started')
    yield
    await app.bot.session.close()
    logger.info('Telegram Bot stopped')

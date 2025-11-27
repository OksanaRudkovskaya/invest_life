import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from model.predict_service import PredictService
from .middlewares import VerifyAuthTokenMiddleware
from .router import router as core_router

from src.predict import router as model_service_router
from settings import VERIFY_TOKEN_MIDDLEWARE

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
    if VERIFY_TOKEN_MIDDLEWARE:
        app.add_middleware(VerifyAuthTokenMiddleware)

    app.include_router(core_router)
    app.include_router(model_service_router, prefix="/api/v1")

    return app


async def lifespan(app: FastAPI):
    logger.info('Loading models...')
    app.predict_service = PredictService()
    logger.info('Models loaded')
    logger.info('Application start')

    yield
    logger.info('Application down')
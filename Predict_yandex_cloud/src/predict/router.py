from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel

from src.core.utils import verify_auth_token
from src.predict.models import RequestData, PredictResponse, PredictTicker


router = APIRouter()


@router.post("/predict", response_model=PredictResponse)
async def predict(data: RequestData, request: Request = None, not_verified = Depends(verify_auth_token)):
    if not_verified:
        return not_verified

    results = []
    for row in data.data:
        preds, probs = request.app.predict_service.predict_last_row(row)
        results.append(
            PredictTicker(
                ticker=row.ticker,
                prediction=preds,
                proba=probs
            )
        )
    resp = PredictResponse(predict=[])
    resp.predict = results
    return resp

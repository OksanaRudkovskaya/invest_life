from pydantic import BaseModel
from typing import List, Union


class VectorDateItem(BaseModel):
    date: str
    vector: List[Union[int, float]]

class DataItem(BaseModel):
    ticker: str
    vectors: List[VectorDateItem]

    def sort_vectors_by_date(self, reverse: bool = False):
        self.vectors.sort(
            key=lambda x: x.date,
            reverse=reverse
        )
        return self

class RequestData(BaseModel):
    data: List[DataItem]


class PredictTicker(BaseModel):
    ticker: str
    prediction: int
    proba: list[float]

class PredictResponse(BaseModel):
    predict: list[PredictTicker]
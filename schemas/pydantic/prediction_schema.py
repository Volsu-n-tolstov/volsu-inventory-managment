from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class PredictionRequestSchema(BaseModel):
    item_ids: List[int]
    prediction_days: int = 365


class PredictionDataSchema(BaseModel):
    date: datetime
    predicted_quantity: float
    lower_bound: float
    upper_bound: float


class PredictionResponseSchema(BaseModel):
    item_id: int
    item_name: str
    predictions: List[PredictionDataSchema]
    status: str
    error: Optional[str] = None

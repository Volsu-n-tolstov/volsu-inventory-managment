from pydantic import BaseModel
from datetime import datetime


class TransactionSchema(BaseModel):
    transaction_id: str
    date: datetime
    item_id: int
    transaction_type: str
    quantity: float
    unit_price: float

    class Config:
        from_attributes = True

import strawberry

from typing import Optional
from datetime import datetime


@strawberry.type
class Transaction:
    transaction_id: str
    date: datetime 
    item_id: str
    transaction_type: str
    quantity: int
    unit_price: float


@strawberry.input
class TransactionInput:
    date: datetime
    item_id: str 
    transaction_type: str
    quantity: int
    unit_price: float


@strawberry.input
class TransactionUpdate:
    transaction_id: str
    date: Optional[datetime] = None
    item_id: Optional[str] = None
    transaction_type: Optional[str] = None 
    quantity: Optional[int] = None
    unit_price: Optional[float] = None

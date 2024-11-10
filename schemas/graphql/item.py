import strawberry

from typing import Optional


@strawberry.type
class Item:
    item_id: int
    item_name: str
    category: str
    supplier: str
    purchase_price: float
    sale_price: float
    units: str
    storage_condition: str
    shelf_life_days: int


@strawberry.input
class ItemInput:
    item_name: str
    category: str
    supplier: str
    purchase_price: float
    sale_price: float
    units: str
    storage_condition: str
    shelf_life_days: int


@strawberry.input
class ItemUpdate:
    item_id: int
    item_name: Optional[str] = None
    category: Optional[str] = None
    supplier: Optional[str] = None
    purchase_price: Optional[float] = None
    sale_price: Optional[float] = None
    units: Optional[str] = None
    storage_condition: Optional[str] = None
    shelf_life_days: Optional[int] = None

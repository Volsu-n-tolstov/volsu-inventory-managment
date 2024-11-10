from pydantic import BaseModel


class ItemSchema(BaseModel):
    item_id: int
    item_name: str
    category: str
    supplier: str
    purchase_price: float
    sale_price: float
    units: str
    storage_condition: str
    shelf_life_days: int

    class Config:
        from_attributes = True


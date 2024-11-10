from sqlalchemy import (
    Column, Integer, 
    String, Float
)

from models.base_model import entity_meta


class ItemModel(entity_meta):
    __tablename__ = "items"

    item_id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    supplier = Column(String(100), nullable=False)
    purchase_price = Column(Float, nullable=False)
    sale_price = Column(Float, nullable=False)
    units = Column(String(50), nullable=False)
    storage_condition = Column(String(100), nullable=False)
    shelf_life_days = Column(Integer, nullable=False)

    def normalize(self) -> dict:
        return {
            "item_id": self.item_id,
            "item_name": self.item_name,
            "category": self.category,
            "supplier": self.supplier,
            "purchase_price": self.purchase_price,
            "sale_price": self.sale_price,
            "units": self.units,
            "storage_condition": self.storage_condition,
            "shelf_life_days": self.shelf_life_days
        }

from sqlalchemy import (
    Column, Integer, String, 
    Float, DateTime
)

from models.base_model import entity_meta


class TransactionModel(entity_meta):
    __tablename__ = "transactions"

    transaction_id = Column(String(36), primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    item_id = Column(String(10), nullable=False)
    transaction_type = Column(String(10), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    def normalize(self) -> dict:
        return {
            "transaction_id": self.transaction_id,
            "date": self.date,
            "item_id": self.item_id,
            "transaction_type": self.transaction_type,
            "quantity": self.quantity,
            "unit_price": self.unit_price
        }

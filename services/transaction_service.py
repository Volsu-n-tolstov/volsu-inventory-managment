from typing import List

from fastapi import Depends

from models.transaction_model import TransactionModel
from repositories.transaction_repository import TransactionRepository


class TransactionService:
    
    def __init__(self, repository: TransactionRepository = Depends(TransactionRepository)) -> None:
        self.repository = repository

    def create_transaction(self, transaction: TransactionModel) -> TransactionModel:
        return self.repository.create(transaction)

    def delete_transaction(self, id: str) -> None:
        self.repository.delete(id)

    def get_transaction(self, id: str) -> TransactionModel:
        return self.repository.get(id)

    def list_transactions(
        self,
        limit: int = None,
        start: int = None,
        item_id: str = None,
        start_date: str = None,
        end_date: str = None
    ) -> List[TransactionModel]:
        return self.repository.list(
            limit=limit,
            start=start,
            item_id=item_id,
            start_date=start_date,
            end_date=end_date
        )

    def update_transaction(self, id: str, transaction: TransactionModel) -> TransactionModel:
        return self.repository.update(id, transaction)

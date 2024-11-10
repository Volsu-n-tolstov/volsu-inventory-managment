from typing import List

from fastapi import Depends

from sqlalchemy.orm import Session

from models.transaction_model import TransactionModel
from repositories.repository_meta import RepositoryMeta
from configs.database import get_db_connection


class TransactionRepository(RepositoryMeta[TransactionModel, str]):

    def __init__(self, session: Session = Depends(get_db_connection)) -> None:
        self.session = session

    def create(self, instance: TransactionModel) -> TransactionModel:
        self.session.add(instance)
        self.session.commit()

        return instance

    def delete(self, id: str) -> None:
        transaction = self.session.query(TransactionModel).filter(TransactionModel.transaction_id == id).first()

        if transaction:
            self.session.delete(transaction)
            self.session.commit()

    def get(self, id: str) -> TransactionModel:
        return self.session.query(TransactionModel).filter(TransactionModel.transaction_id == id).first()

    def list(
        self,
        limit: int = None,
        start: int = None,
        item_id: str = None,
        start_date: str = None,
        end_date: str = None
    ) -> List[TransactionModel]:
        query = self.session.query(TransactionModel)
        
        if item_id:
            query = query.filter(TransactionModel.item_id == item_id)
            
        if start_date:
            query = query.filter(TransactionModel.date >= start_date)
            
        if end_date:
            query = query.filter(TransactionModel.date <= end_date)
            
        if start is not None:
            query = query.offset(start)
            
        if limit is not None:
            query = query.limit(limit)
            
        return query.all()

    def update(self, id: str, instance: TransactionModel) -> TransactionModel:
        transaction = self.session.query(TransactionModel).filter(TransactionModel.transaction_id == id).first()

        if transaction:
            for key, value in instance.normalize().items():
                if value is not None:
                    setattr(transaction, key, value)

            self.session.commit()
            return transaction
        
        return None

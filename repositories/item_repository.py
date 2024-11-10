from typing import List

from fastapi import Depends

from sqlalchemy.orm import Session

from models.item_model import ItemModel
from repositories.repository_meta import RepositoryMeta
from configs.database import get_db_connection


class ItemRepository(RepositoryMeta[ItemModel, int]):

    def __init__(self, session: Session = Depends(get_db_connection)) -> None:
        self.session = session

    def create(self, instance: ItemModel) -> ItemModel:
        self.session.add(instance)
        self.session.commit()
        
        return instance

    def delete(self, id: int) -> None:
        item = self.session.query(ItemModel).filter(ItemModel.item_id == id).first()

        if item:
            self.session.delete(item)
            self.session.commit()

    def get(self, id: int) -> ItemModel:
        return self.session.query(ItemModel).filter(ItemModel.item_id == id).first()

    def list(self, limit: int = None, start: int = None) -> List[ItemModel]:
        query = self.session.query(ItemModel)

        if start is not None:
            query = query.offset(start)
            
        if limit is not None:
            query = query.limit(limit)

        return query.all()

    def update(self, id: int, instance: ItemModel) -> ItemModel:
        item = self.session.query(ItemModel).filter(ItemModel.item_id == id).first()

        if item:
            for key, value in instance.normalize().items():
                if value is not None:
                    setattr(item, key, value)
            self.session.commit()
            return item
        
        return None

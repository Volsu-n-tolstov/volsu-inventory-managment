from typing import List

from fastapi import Depends

from models.item_model import ItemModel
from repositories.item_repository import ItemRepository


class ItemService:
    
    def __init__(self, repository: ItemRepository = Depends(ItemRepository)) -> None:
        self.repository = repository

    def create_item(self, item: ItemModel) -> ItemModel:
        return self.repository.create(item)

    def delete_item(self, id: int) -> None:
        self.repository.delete(id)

    def get_item(self, id: int) -> ItemModel:
        return self.repository.get(id)

    def list_items(self, limit: int = None, start: int = None) -> List[ItemModel]:
        return self.repository.list(limit=limit, start=start)

    def update_item(self, id: int, item: ItemModel) -> ItemModel:
        return self.repository.update(id, item)

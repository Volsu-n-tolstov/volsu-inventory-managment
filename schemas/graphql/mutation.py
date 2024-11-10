import strawberry
from strawberry.types import Info

from typing import Optional

from models.item_model import ItemModel
from models.transaction_model import TransactionModel
from configs.graphql import get_item_service, get_transaction_service
from schemas.graphql.item import Item, ItemInput
from schemas.graphql.transaction import Transaction, TransactionInput


@strawberry.type
class Mutation:
    
    @strawberry.mutation
    def create_item(self, item: ItemInput, info: Info) -> Item:
        service = get_item_service(info)
        item_model = ItemModel(**item.__dict__)
        created_item = service.create_item(item_model)
        return Item.from_model(created_item)

    @strawberry.mutation
    def update_item(self, id: int, item: ItemInput, info: Info) -> Optional[Item]:
        service = get_item_service(info)
        item_model = ItemModel(**item.__dict__)
        updated_item = service.update_item(id, item_model)
        return Item.from_model(updated_item) if updated_item else None

    @strawberry.mutation
    def delete_item(self, id: int, info: Info) -> bool:
        service = get_item_service(info)
        service.delete_item(id)
        return True

    @strawberry.mutation
    def create_transaction(self, transaction: TransactionInput, info: Info) -> Transaction:
        service = get_transaction_service(info)
        transaction_model = TransactionModel(**transaction.__dict__)
        created_transaction = service.create_transaction(transaction_model)
        return Transaction.from_model(created_transaction)

    @strawberry.mutation
    def update_transaction(self, id: str, transaction: TransactionInput, info: Info) -> Optional[Transaction]:
        service = get_transaction_service(info)
        transaction_model = TransactionModel(**transaction.__dict__)
        updated_transaction = service.update_transaction(id, transaction_model)
        return Transaction.from_model(updated_transaction) if updated_transaction else None

    @strawberry.mutation
    def delete_transaction(self, id: str, info: Info) -> bool:
        service = get_transaction_service(info)
        service.delete_transaction(id)
        return True

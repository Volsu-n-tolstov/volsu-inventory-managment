import strawberry
from strawberry.types import Info

from typing import List, Optional

from schemas.graphql.item import Item
from schemas.graphql.transaction import Transaction
from configs.graphql import get_item_service, get_transaction_service


@strawberry.type
class Query:
    @strawberry.field
    def item(self, id: int, info: Info) -> Optional[Item]:
        service = get_item_service(info)
        item = service.get_item(id)
        return Item.from_model(item) if item else None

    @strawberry.field
    def items(
        self,
        limit: Optional[int] = None,
        start: Optional[int] = None,
        info: Info = None
    ) -> List[Item]:
        service = get_item_service(info)
        items = service.list_items(limit=limit, start=start)
        return [Item.from_model(item) for item in items]

    @strawberry.field
    def transaction(self, id: str, info: Info) -> Optional[Transaction]:
        service = get_transaction_service(info)
        transaction = service.get_transaction(id)
        return Transaction.from_model(transaction) if transaction else None

    @strawberry.field
    def transactions(
        self,
        limit: Optional[int] = None,
        start: Optional[int] = None,
        item_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        info: Info = None
    ) -> List[Transaction]:
        service = get_transaction_service(info)
        transactions = service.list_transactions(
            limit=limit,
            start=start,
            item_id=item_id,
            start_date=start_date,
            end_date=end_date
        )
        return [Transaction.from_model(transaction) for transaction in transactions]

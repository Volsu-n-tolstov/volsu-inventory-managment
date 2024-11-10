from fastapi import Depends
from strawberry.types import Info

from services.transaction_service import TransactionService
from services.item_service import ItemService


async def get_graphql_context(
    transaction_service: TransactionService = Depends(),
    item_service: ItemService = Depends()
) -> dict:
    return {
        "transaction_service": transaction_service,
        "item_service": item_service
    }


def get_transaction_service(info: Info) -> TransactionService:
    return info.context["transaction_service"]


def get_item_service(info: Info) -> ItemService:
    return info.context["item_service"]


from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from services.transaction_service import TransactionService
from models.transaction_model import TransactionModel
from schemas.pydantic.transaction_schema import TransactionSchema
from middlewares.auth import token_auth

router = APIRouter(
    prefix="/api/v1/transactions",
    tags=["transactions"],
    dependencies=[Depends(token_auth)]
)


@router.post("", response_model=TransactionSchema, status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction: TransactionSchema, service: TransactionService = Depends()) -> TransactionSchema:
    transaction_model = TransactionModel(**transaction.model_dump())
    return service.create_transaction(transaction_model)


@router.get("/{transaction_id}", response_model=TransactionSchema)
async def get_transaction(transaction_id: int, service: TransactionService = Depends()) -> TransactionSchema:
    transaction = service.get_transaction(transaction_id)

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id {transaction_id} not found"
        )
    
    return transaction


@router.get("", response_model=List[TransactionSchema])
async def list_transactions(
    limit: int = None,
    start: int = None,
    item_id: str = None,
    start_date: str = None,
    end_date: str = None,
    service: TransactionService = Depends()
) -> List[TransactionSchema]:
    return service.list_transactions(
        limit=limit,
        start=start,
        item_id=item_id,
        start_date=start_date,
        end_date=end_date
    )


@router.put("/{transaction_id}", response_model=TransactionSchema)
async def update_transaction(
    transaction_id: int,
    transaction: TransactionSchema,
    service: TransactionService = Depends()
) -> TransactionSchema:
    transaction_model = TransactionModel(**transaction.model_dump())
    updated_transaction = service.update_transaction(transaction_id, transaction_model)

    if not updated_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id {transaction_id} not found"
        )

    return updated_transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: int, service: TransactionService = Depends()) -> None:
    transaction = service.get_transaction(transaction_id)

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id {transaction_id} not found"
        )

    service.delete_transaction(transaction_id)

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from services.item_service import ItemService
from models.item_model import ItemModel
from schemas.pydantic.item_schema import ItemSchema
from middlewares.auth import token_auth

router = APIRouter(
    prefix="/api/v1/items",
    tags=["items"],
    dependencies=[Depends(token_auth)]
)


@router.post("", response_model=ItemSchema, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemSchema, service: ItemService = Depends()) -> ItemSchema:
    item_model = ItemModel(**item.model_dump())
    return service.create_item(item_model)


@router.get("/{item_id}", response_model=ItemSchema)
async def get_item(item_id: int, service: ItemService = Depends()) -> ItemSchema:
    item = service.get_item(item_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    
    return item


@router.get("", response_model=List[ItemSchema])
async def list_items(
    limit: int = None,
    start: int = None,
    service: ItemService = Depends()
) -> List[ItemSchema]:
    return service.list_items(limit=limit, start=start)


@router.put("/{item_id}", response_model=ItemSchema)
async def update_item(
    item_id: int,
    item: ItemSchema,
    service: ItemService = Depends()
) -> ItemSchema:
    item_model = ItemModel(**item.model_dump())
    updated_item = service.update_item(item_id, item_model)

    if not updated_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )

    return updated_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, service: ItemService = Depends()) -> None:
    item = service.get_item(item_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )

    service.delete_item(item_id)

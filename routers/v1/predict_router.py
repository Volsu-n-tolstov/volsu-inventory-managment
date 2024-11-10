import pandas as pd

from fastapi import APIRouter, HTTPException, Depends
from typing import List

from middlewares.auth import token_auth
from services.item_service import ItemService
from services.transaction_service import TransactionService
from utils.predict import prepare_data_from_db, predict_usage
from schemas.pydantic.prediction_schema import (
    PredictionRequestSchema,
    PredictionResponseSchema,
    PredictionDataSchema
)

router = APIRouter(
    prefix="/api/v1/predict", 
    tags=["predict"],
    dependencies=[Depends(token_auth)]
)


@router.post("/", response_model=List[PredictionResponseSchema])
async def create_predictions(
    request: PredictionRequestSchema,
    item_service: ItemService = Depends(),
    transaction_service: TransactionService = Depends()
):
    if not 1 <= request.prediction_days <= 365:
        raise HTTPException(
            status_code=400,
            detail="Количество дней для прогнозирования должно быть от 1 до 365"
        )

    responses = []
    
    try:
        # Получаем все транзакции
        transactions = transaction_service.list_transactions()
        if not transactions:
            raise HTTPException(
                status_code=400,
                detail="Нет данных о транзакциях"
            )
        transactions_df = pd.DataFrame([t.normalize() for t in transactions])
        
        # Добавляем проверку данных
        print(f"Transactions shape: {transactions_df.shape}")
        print(f"Transactions columns: {transactions_df.columns}")
        print(f"Transactions date range: {transactions_df['date'].min()} - {transactions_df['date'].max()}")
        
        # Получаем все товары
        items = item_service.list_items()
        if not items:
            raise HTTPException(
                status_code=400,
                detail="Нет данных о товарах"
            )
        items_df = pd.DataFrame([i.normalize() for i in items])
        
        # Подготавливаем данные из БД
        daily_usage = prepare_data_from_db(transactions_df, items_df)
        
        for item_id in request.item_ids:
            try:
                # Получаем информацию о товаре
                item = item_service.get_item(item_id)
                if not item:
                    raise HTTPException(status_code=404, detail=f"Товар с ID {item_id} не найден")
                
                # Получаем данные для конкретного товара
                item_data = daily_usage[daily_usage['item_name'] == item.item_name].copy()
                if len(item_data) < 2:
                    raise ValueError("Недостаточно данных для прогнозирования")
                
                # Подготавливаем данные для Prophet
                item_data.columns = ['ds', 'item_name', 'y']
                
                # Прогнозирование
                forecast = predict_usage(daily_usage, item.item_name, periods=request.prediction_days)
                
                # Преобразуем прогноз в список PredictionData
                predictions = []
                last_date = item_data['ds'].max()
                future_forecast = forecast[forecast['ds'] > last_date]
                
                for _, row in future_forecast.iterrows():
                    predictions.append(PredictionDataSchema(
                        date=row['ds'],
                        predicted_quantity=max(0, float(row['yhat'])),
                        lower_bound=max(0, float(row['yhat_lower'])),
                        upper_bound=max(0, float(row['yhat_upper']))
                    ))
                
                responses.append(PredictionResponseSchema(
                    item_id=item_id,
                    item_name=item.item_name,
                    predictions=predictions,
                    status="success"
                ))
            except Exception as e:
                responses.append(PredictionResponseSchema(
                    item_id=item_id,
                    item_name=item.item_name if item else "Unknown",
                    predictions=[],
                    status="error",
                    error=str(e)
                ))
                
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при подготовке данных: {str(e)}"
        )

    return responses

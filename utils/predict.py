import pandas as pd
from prophet import Prophet
from typing import List, Optional
from datetime import datetime

from models.transaction_model import TransactionModel
from models.item_model import ItemModel


def prepare_data_from_db(
    transactions_df: pd.DataFrame,
    items_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Подготавливает данные из БД для прогнозирования
    
    Args:
        transactions_df: DataFrame с транзакциями из БД
        items_df: DataFrame с товарами из БД
        
    Returns:
        DataFrame с подготовленными данными для прогнозирования
    """
    # Приводим item_id к одному типу
    transactions_df['item_id'] = transactions_df['item_id'].astype(str)
    items_df['item_id'] = items_df['item_id'].astype(str)
    
    # Преобразуем дату и округляем до дня
    transactions_df['date'] = pd.to_datetime(transactions_df['date']).dt.floor('D')
    
    # Объединение данных
    df = transactions_df.merge(items_df, on='item_id')
    
    # Группировка по дате (округленной до дня) и подсчет количества
    daily_usage = df.groupby(['date', 'item_name'])['quantity'].sum().reset_index()
    
    if len(daily_usage) > 0:
        # Получаем диапазон дат
        min_date = daily_usage['date'].min()
        max_date = daily_usage['date'].max()
        
        # Создаем полный диапазон дат
        date_range = pd.date_range(start=min_date, end=max_date, freq='D')
        items = daily_usage['item_name'].unique()
        
        # Создаем все возможные комбинации дат и товаров
        dates_items = pd.MultiIndex.from_product(
            [date_range, items],
            names=['date', 'item_name']
        )
        
        # Преобразуем в DataFrame и заполняем пропуски нулями
        daily_usage = (daily_usage
                      .set_index(['date', 'item_name'])
                      .reindex(dates_items, fill_value=0)
                      .reset_index())
        
        print(f"Prepared data shape: {daily_usage.shape}")
        print(f"Unique items: {daily_usage['item_name'].unique()}")
        print(f"Date range: {daily_usage['date'].min()} - {daily_usage['date'].max()}")
        print(f"Sample data:\n{daily_usage.head()}")
        
        return daily_usage
    else:
        return pd.DataFrame(columns=['date', 'item_name', 'quantity'])


def prepare_data_from_models(
    transactions: List[TransactionModel],
    items: List[ItemModel]
) -> pd.DataFrame:
    # Преобразование моделей в датафреймы
    transactions_df = pd.DataFrame([t.normalize() for t in transactions])
    items_df = pd.DataFrame([i.normalize() for i in items])
    
    # Преобразование столбца date в формат datetime
    transactions_df['date'] = pd.to_datetime(transactions_df['date'])
    
    # Объединение данных
    df = transactions_df.merge(items_df, on='item_id')
    
    # Группировка по дате и подсчет количества использований
    daily_usage = df.groupby(['date', 'item_name'])['quantity'].sum().reset_index()
    return daily_usage


def create_holidays():
    holidays_list = []
    
    # Новый год
    new_year = pd.DataFrame({
        'holiday': 'new_year',
        'ds': pd.date_range(start='2015-12-31', end='2026-01-08', freq='YE-DEC'),
        'lower_window': 0,
        'upper_window': 8
    })
    holidays_list.append(new_year)
    
    # День святого Валентина
    valentine = pd.DataFrame({
        'holiday': 'valentine',
        'ds': pd.date_range(start='2015-02-14', end='2026-02-14', freq='YE-FEB'),
        'lower_window': -2,
        'upper_window': 0
    })
    holidays_list.append(valentine)
    
    # День защитника Отечества
    defender = pd.DataFrame({
        'holiday': 'defender',
        'ds': pd.date_range(start='2015-02-23', end='2026-02-23', freq='YE-FEB'),
        'lower_window': -3,
        'upper_window': 1
    })
    holidays_list.append(defender)
    
    # 8 марта
    march_8 = pd.DataFrame({
        'holiday': 'march_8',
        'ds': pd.date_range(start='2015-03-08', end='2026-03-08', freq='YE-MAR'),
        'lower_window': -3,
        'upper_window': 1
    })
    holidays_list.append(march_8)
    
    # День космонавтики
    cosmonaut = pd.DataFrame({
        'holiday': 'cosmonaut',
        'ds': pd.date_range(start='2015-04-12', end='2026-04-12', freq='YE-APR'),
        'lower_window': -1,
        'upper_window': 1
    })
    holidays_list.append(cosmonaut)
    
    # Майские праздники
    may_holidays = pd.DataFrame({
        'holiday': 'may_holidays',
        'ds': pd.date_range(start='2015-05-01', end='2026-05-01', freq='YE-MAY'),
        'lower_window': 0,
        'upper_window': 9
    })
    holidays_list.append(may_holidays)
    
    # День защиты детей
    children = pd.DataFrame({
        'holiday': 'children',
        'ds': pd.date_range(start='2015-06-01', end='2026-06-01', freq='YE-JUN'),
        'lower_window': -1,
        'upper_window': 1
    })
    holidays_list.append(children)
    
    # День России
    russia = pd.DataFrame({
        'holiday': 'russia',
        'ds': pd.date_range(start='2015-06-12', end='2026-06-12', freq='YE-JUN'),
        'lower_window': -2,
        'upper_window': 1
    })
    holidays_list.append(russia)
    
    # День семьи
    family = pd.DataFrame({
        'holiday': 'family',
        'ds': pd.date_range(start='2015-07-08', end='2026-07-08', freq='YE-JUL'),
        'lower_window': -1,
        'upper_window': 1
    })
    holidays_list.append(family)
    
    # День знаний
    knowledge = pd.DataFrame({
        'holiday': 'knowledge',
        'ds': pd.date_range(start='2015-09-01', end='2026-09-01', freq='YE-SEP'),
        'lower_window': -7,
        'upper_window': 0
    })
    holidays_list.append(knowledge)
    
    # День народного единства
    unity = pd.DataFrame({
        'holiday': 'unity',
        'ds': pd.date_range(start='2015-11-04', end='2026-11-04', freq='YE-NOV'),
        'lower_window': -2,
        'upper_window': 1
    })
    holidays_list.append(unity)
    
    # День Конституции
    constitution = pd.DataFrame({
        'holiday': 'constitution',
        'ds': pd.date_range(start='2015-12-12', end='2026-12-12', freq='YE-DEC'),
        'lower_window': -1,
        'upper_window': 1
    })
    holidays_list.append(constitution)
    
    holidays = pd.concat(holidays_list)
    return holidays


def predict_usage(
    daily_usage: pd.DataFrame,
    item_name: str,
    periods: int = 365
) -> pd.DataFrame:
    # Получаем данные для конкретного товара
    item_data = daily_usage[daily_usage['item_name'] == item_name].copy()
    print(f"Data for item {item_name}:")
    print(f"Shape: {item_data.shape}")
    print(f"Date range: {item_data['date'].min()} - {item_data['date'].max()}")
    print(f"Number of non-zero values: {(item_data['quantity'] > 0).sum()}")
    
    if len(item_data) < 2:
        raise ValueError("Недостаточно данных для прогнозирования")
    
    # Переименовываем колонки для Prophet
    item_data.columns = ['ds', 'item_name', 'y']
    
    # Создаем и настраиваем модель
    model = Prophet(
        holidays=create_holidays(),
        yearly_seasonality=20,
        weekly_seasonality=True,
        daily_seasonality=True,
        seasonality_mode='multiplicative',
        changepoint_prior_scale=0.05,
        holidays_prior_scale=10
    )
    
    model.fit(item_data)
    
    # Создаем датафрейм для прогноза
    last_date = item_data['ds'].max()
    future_dates = model.make_future_dataframe(periods=periods)
    future_dates = future_dates[future_dates['ds'] > last_date]
    
    forecast = model.predict(future_dates)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

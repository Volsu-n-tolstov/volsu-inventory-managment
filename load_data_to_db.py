import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

from configs.database import DATABASE_URL

def load_data_to_db():
    try:
        engine = create_engine(DATABASE_URL)
        
        # Загружаем данные из CSV
        items_df = pd.read_csv('items.csv')
        transactions_df = pd.read_csv('transactions.csv')
        
        # Преобразуем item_id в items_df (убираем префикс 'ITEM' и конвертируем в int)
        items_df['item_id'] = items_df['item_id'].str.replace('ITEM', '').astype(int)
        
        # Обновляем item_id в transactions_df соответственно
        transactions_df['item_id'] = transactions_df['item_id'].str.replace('ITEM', '').astype(int)
        
        # Преобразуем дату в правильный формат для PostgreSQL
        transactions_df['date'] = pd.to_datetime(transactions_df['date'])
        
        # Загружаем данные в БД
        items_df.to_sql('items', engine, if_exists='append', index=False)
        print("Таблица items успешно заполнена")
        
        transactions_df.to_sql('transactions', engine, if_exists='append', index=False)
        print("Таблица transactions успешно заполнена")
        
        print("Загрузка данных завершена успешно!")
        
    except Exception as e:
        print(f"Произошла ошибка при загрузке данных: {str(e)}")

if __name__ == "__main__":
    load_data_to_db()

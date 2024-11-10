import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import uuid
import matplotlib.pyplot as plt

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Генерация 100 товаров
def generate_items():
    categories = ['Electronics', 'Food', 'Clothing', 'Home', 'Beauty', 'Sports', 'Books', 'Toys', 'Garden', 'Auto']
    suppliers = ['Supplier A', 'Supplier B', 'Supplier C', 'Supplier D', 'Supplier E']
    storage_conditions = ['Normal', 'Refrigerated', 'Frozen', 'Cool', 'Warm']
    
    items = []
    for i in range(1, 101):
        category = random.choice(categories)
        base_price = random.uniform(10, 1000)
        items.append({
            'item_id': f'ITEM{i}',
            'item_name': f'Товар {i}',
            'category': category,
            'supplier': random.choice(suppliers),
            'purchase_price': base_price,
            'sale_price': base_price * random.uniform(1.3, 1.8),
            'units': 'units' if category != 'Food' else random.choice(['kg', 'units']),
            'storage_condition': random.choice(storage_conditions),
            'shelf_life_days': random.randint(30, 730),
        })
    return pd.DataFrame(items)

def is_russian_holiday(date):
    # Расширенный список праздников
    holidays = [
        (1, 1),   # Новый год
        (1, 2),   # Новогодние каникулы
        (1, 3),   # Новогодние каникулы
        (1, 4),   # Новогодние каникулы
        (1, 5),   # Новогодние каникулы
        (1, 6),   # Новогодние каникулы
        (1, 7),   # Рождество Христово
        (1, 8),   # Новогодние каникулы
        (2, 14),  # День святого Валентина
        (2, 23),  # День защитника Отечества
        (3, 8),   # Международный женский день
        (4, 12),  # День космонавтики
        (5, 1),   # Праздник Весны и Труда
        (5, 9),   # День Победы
        (6, 1),   # День защиты детей
        (6, 12),  # День России
        (7, 8),   # День семьи, любви и верности
        (8, 22),  # День государственного флага
        (9, 1),   # День знаний
        (10, 5),  # День учителя
        (11, 4),  # День народного единства
        (11, 27), # День матери
        (12, 12), # День Конституции
        (12, 31), # Канун Нового года
    ]
    return (date.month, date.day) in holidays

# Генерация транзакций за 10 лет
def generate_transactions(items_df, start_date, end_date):
    date_range = pd.date_range(start=start_date, end=end_date)
    transactions = []
    
    for date in date_range:
        month = date.month
        weekday = date.weekday()
        is_holiday = is_russian_holiday(date)
        
        for _, item in items_df.iterrows():
            # Базовый спрос и сезонность для каждого товара
            category = item['category']
            if category == 'Electronics':
                base_demand = random.randint(20, 40)
                seasonal_factor = 1.5 if month in [11, 12] else 1.0
                if (month == 2 and date.day in range(15, 24)) or (month == 3 and date.day in range(1, 9)):
                    seasonal_factor *= 1.8
            elif category == 'Food':
                base_demand = random.randint(40, 60)
                seasonal_factor = 1.2 if month in [6, 7, 8] else 1.0
                if month == 12 and date.day > 15:
                    seasonal_factor *= 2.0
            else:
                base_demand = random.randint(10, 100)
                seasonal_factor = 1.0 + 0.3 * np.sin(2 * np.pi * (date.dayofyear / 365))
            
            # Праздничный фактор
            holiday_factor = 1.8 if is_holiday else 1.0
            
            # Предпраздничный фактор (за 5 дней до праздника)
            for h_month, h_day in [(m, d) for m, d in [(1,1), (12,31), (2,23), (3,8), (5,9), (6,12), (11,4)]]:
                holiday_date = datetime(date.year, h_month, h_day).date()
                days_until_holiday = (holiday_date - date.date()).days
                if 0 <= days_until_holiday <= 5:
                    holiday_factor = 1.5
            
            # Тренд (увеличение спроса на 20% за 10 лет)
            days_since_start = (date - start_date).days
            trend_factor = 1 + (days_since_start / 3650) * 0.2
            
            # Случайные колебания
            random_factor = np.random.normal(1, 0.15)
            
            # Расчет спроса с учетом праздников
            demand = base_demand * seasonal_factor * trend_factor * random_factor * holiday_factor
            demand = max(0, int(demand))
            
            if demand > 0:
                # Исходящие транзакции (продажи)
                transactions.append({
                    'transaction_id': str(uuid.uuid4()),
                    'date': date,
                    'item_id': item['item_id'],
                    'transaction_type': 'Outbound',
                    'quantity': demand,
                    'unit_price': item['sale_price'],
                })
                
                # Входящие транзакции (пополнение) с учетом праздников
                restock_quantity = int(demand * 1.2) if is_holiday else demand + random.randint(0, 5)
                transactions.append({
                    'transaction_id': str(uuid.uuid4()),
                    'date': date,
                    'item_id': item['item_id'],
                    'transaction_type': 'Inbound',
                    'quantity': restock_quantity,
                    'unit_price': item['purchase_price'],
                })
    
    return pd.DataFrame(transactions)

def plot_usage_history(transactions_df):
    plt.figure(figsize=(15, 10))
    
    # Группировка данных по датам и категориям для исходящих транзакций
    daily_usage = transactions_df[transactions_df['transaction_type'] == 'Outbound'].groupby(
        ['date', 'item_id'])['quantity'].sum().reset_index()
    
    # Выбираем случайные 5 товаров для отображения
    sample_items = random.sample(daily_usage['item_id'].unique().tolist(), 5)
    
    # Построение графиков для выбранных товаров
    for item_id in sample_items:
        item_data = daily_usage[daily_usage['item_id'] == item_id]
        plt.plot(item_data['date'], item_data['quantity'], 
                label=f'Товар {item_id[4:]}',
                alpha=0.7)
    
    plt.title('История использования товаров за 10 лет\n(с учетом российских праздников)')
    plt.xlabel('Дата')
    plt.ylabel('Количество')
    plt.legend()
    plt.grid(True)
    plt.savefig('usage_history.png')
    plt.close()

def main():
    start_date = datetime.now() - timedelta(days=3650)  # 10 лет назад
    end_date = datetime.now()

    items_df = generate_items()
    transactions_df = generate_transactions(items_df, start_date, end_date)

    # Сохранение в CSV
    items_df.to_csv('items.csv', index=False)
    transactions_df.to_csv('transactions.csv', index=False)
    
    # Построение графика
    plot_usage_history(transactions_df)
    
    print("Генерация данных завершена. Сохранены файлы: 'items.csv', 'transactions.csv' и 'usage_history.png'")

if __name__ == "__main__":
    main()

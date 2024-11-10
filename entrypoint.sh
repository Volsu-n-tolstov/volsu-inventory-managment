#!/bin/bash

# # Генерируем UUID для названия миграции
# MIGRATION_ID=$(python -c "import uuid; print(str(uuid.uuid4()))")

# # Создаем ревизию, если есть изменения
# echo "Creating new migration if there are changes..."
# alembic revision --autogenerate -m "$MIGRATION_ID"

# Применяем миграции
echo "Applying migrations..."
alembic upgrade head

# Запускаем приложение
echo "Starting application..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
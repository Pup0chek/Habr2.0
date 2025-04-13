# content-service/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Копируем файл зависимостей и устанавливаем библиотеки
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем исходный код
COPY . .

# При старте сначала выполняем скрипт создания таблиц, затем запускаем приложение
CMD ["sh", "-c", "python -m create_tables && uvicorn app.main:app --host 0.0.0.0 --port 8002"]

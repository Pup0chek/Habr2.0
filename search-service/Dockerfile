FROM python:3.9-slim

WORKDIR /app

# Копируем файл зависимостей и устанавливаем пакеты
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем исходный код
COPY . .

# Запускаем приложение через uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]

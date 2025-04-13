# gateway/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Копируем файлы зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip install requests

# Копируем исходный код
COPY . .

# Указываем команду запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

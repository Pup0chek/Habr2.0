# content-service/app/main.py
import os
import json
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models import Base, Article
import pika

# Читаем переменную окружения для подключения к БД
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/articles_db")

# Создаем движок и сессию SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI(title="Content Service", description="Сервис управления статьями", version="1.0.0")

# Pydantic-модель для создания статьи
class ArticleCreate(BaseModel):
    title: str
    content: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Функция для публикации сообщения в RabbitMQ
def publish_article_event(article: dict):
    RABBITMQ_URL = os.environ.get("RABBITMQ_URL", "amqp://rabbitmq")
    QUEUE_NAME = "article_created"
    try:
        params = pika.URLParameters(RABBITMQ_URL)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        # Обеспечиваем существование очереди
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        message = json.dumps(article)
        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # сообщение устойчиво
            )
        )
        connection.close()
    except Exception as e:
        print("Error publishing message:", e)

@app.post("/articles")
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = Article(title=article.title, content=article.content)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    # После сохранения в БД публикуем событие в RabbitMQ
    publish_article_event({
        "id": db_article.id,
        "title": db_article.title,
        "content": db_article.content,
        "timestamp": db_article.timestamp.isoformat()
    })
    return {
        "id": db_article.id,
        "title": db_article.title,
        "content": db_article.content,
        "timestamp": db_article.timestamp.isoformat()
    }

@app.get("/articles")
def read_articles(db: Session = Depends(get_db)):
    articles = db.query(Article).all()
    result = []
    for a in articles:
        result.append({
            "id": a.id,
            "title": a.title,
            "content": a.content,
            "timestamp": a.timestamp.isoformat() if a.timestamp else None
        })
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8002, reload=True)

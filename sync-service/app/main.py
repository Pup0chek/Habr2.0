import json
import os
import pika
from elasticsearch import Elasticsearch
from time import sleep

# Получаем переменные окружения
RABBITMQ_URL = os.environ.get("RABBITMQ_URL", "amqp://rabbitmq")
ELASTIC_URL = os.environ.get("ELASTIC_URL", "http://elasticsearch:9200")
QUEUE_NAME = "article_created"

# Создаем подключение к Elasticsearch
es = Elasticsearch(ELASTIC_URL)

def callback(ch, method, properties, body):
    try:
        article = json.loads(body)
        # Ожидается, что сообщение содержит идентификатор статьи и её поля
        # Пример: {"id": 1, "content": "...", "title": "...", "timestamp": "...", "tags": [...]}
        res = es.index(index="documents", id=article.get("id"), body=article)
        print("Indexed article:", res)
    except Exception as e:
        print("Error processing message:", e)

def main():
    connection = None
    while connection is None:
        try:
            params = pika.URLParameters(RABBITMQ_URL)
            connection = pika.BlockingConnection(params)
        except Exception as e:
            print("Waiting for RabbitMQ...", e)
            sleep(5)
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
    print(f" [*] Waiting for messages in queue '{QUEUE_NAME}'. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    main()

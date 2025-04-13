# content-service/create_tables.py
from app.models import Base
from sqlalchemy import create_engine
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/articles_db")
engine = create_engine(DATABASE_URL)

if __name__ == "__main__":
    Base.metadata.create_all(engine)

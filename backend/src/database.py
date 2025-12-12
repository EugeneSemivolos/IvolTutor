# backend/src/database.py
from sqlmodel import SQLModel, create_engine, Session
import os

# Отримуємо посилання на БД зі змінних оточення (з docker-compose)
# Якщо змінної немає (локальний запуск), використовуємо дефолтне значення
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/tutor_db")

# Створюємо "двигун" бази даних
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    """Функція-залежність для отримання сесії БД в ендпоінтах"""
    with Session(engine) as session:
        yield session

def init_db():
    """Створює таблиці, якщо їх ще немає"""
    SQLModel.metadata.create_all(engine)
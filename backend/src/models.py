# backend/src/models.py
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
import uuid

# --- 1. Учні ---
class Student(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    full_name: str
    parent_name: Optional[str] = None
    
    # Тут будемо зберігати лінк (https://t.me/username) або просто нік
    telegram_contact: Optional[str] = None 
    
    default_price: float = Field(default=0.0)
    comment: Optional[str] = None
    
    # Зв'язки (для зручності в коді)
    lessons: List["Lesson"] = Relationship(back_populates="student")
    transactions: List["Transaction"] = Relationship(back_populates="student")

# --- 2. Уроки ---
class Lesson(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    student_id: uuid.UUID = Field(foreign_key="student.id")
    
    # Поля для календаря
    start_time: datetime
    end_time: datetime 
    
    topic: Optional[str] = None
    status: str = Field(default="planned")  # planned, completed, cancelled
    price: float  # Ціна конкретного уроку (може відрізнятися від дефолтної)
    
    student: Optional[Student] = Relationship(back_populates="lessons")
    homeworks: List["Homework"] = Relationship(back_populates="lesson")

# --- 3. Оплати (Транзакції) ---
class Transaction(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    student_id: uuid.UUID = Field(foreign_key="student.id")
    
    amount: float
    date: datetime = Field(default_factory=datetime.utcnow)
    comment: Optional[str] = None
    
    student: Optional[Student] = Relationship(back_populates="transactions")

# --- 4. Домашні завдання ---
class Homework(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    lesson_id: uuid.UUID = Field(foreign_key="lesson.id")
    
    description: str
    file_path: Optional[str] = None  # Шлях до файлу на сервері
    
    lesson: Optional[Lesson] = Relationship(back_populates="homeworks")
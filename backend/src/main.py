# backend/src/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List

from .database import init_db, get_session
from .models import Student, Lesson

app = FastAPI(title="Tutor CRM API")

# --- Налаштування CORS (Щоб React бачив Python) ---
origins = [
    "http://localhost:5173",  # Порт Vite (Frontend)
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Подія запуску ---
@app.on_event("startup")
def on_startup():
    init_db()  # Створити таблиці в БД автоматично

# --- Базові Ендпоінти (Приклади) ---

@app.get("/")
def read_root():
    return {"message": "Tutor CRM API is running!"}

# Отримати всіх учнів
@app.get("/students/", response_model=List[Student])
def read_students(session: Session = Depends(get_session)):
    students = session.exec(select(Student)).all()
    return students

# Створити учня
@app.post("/students/", response_model=Student)
def create_student(student: Student, session: Session = Depends(get_session)):
    session.add(student)
    session.commit()
    session.refresh(student)
    return student
# backend/src/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List
from datetime import datetime

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


# 1. Отримати список уроків (з фільтром по датах)
@app.get("/lessons/", response_model=List[Lesson])
def get_lessons(
    start: datetime, 
    end: datetime, 
    session: Session = Depends(get_session)
):
    statement = select(Lesson).where(
        Lesson.start_time >= start,
        Lesson.start_time <= end
    )
    results = session.exec(statement).all()
    return results

# 2. Створити новий урок
@app.post("/lessons/", response_model=Lesson)
def create_lesson(lesson: Lesson, session: Session = Depends(get_session)):
    # Перевіряємо, чи існує студент
    student = session.get(Student, lesson.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
        
    session.add(lesson)
    session.commit()
    session.refresh(lesson)
    return lesson

# 3. Перенести урок (Drag-and-Drop)
@app.patch("/lessons/{lesson_id}", response_model=Lesson)
def update_lesson_date(
    lesson_id: str, 
    lesson_data: dict, # Отримуємо тільки те, що змінилося (start/end)
    session: Session = Depends(get_session)
):
    lesson = session.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Оновлюємо поля
    if "start_time" in lesson_data:
        lesson.start_time = datetime.fromisoformat(lesson_data["start_time"].replace("Z", "+00:00"))
    if "end_time" in lesson_data:
        lesson.end_time = datetime.fromisoformat(lesson_data["end_time"].replace("Z", "+00:00"))
        
    session.add(lesson)
    session.commit()
    session.refresh(lesson)
    return lesson
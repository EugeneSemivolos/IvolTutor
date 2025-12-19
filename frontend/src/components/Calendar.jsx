import React, { useState, useEffect } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import axios from 'axios';

// Базовий URL нашого API
const API_URL = 'http://localhost:8000';

export default function Calendar() {
  const [events, setEvents] = useState([]);

  // Ця функція викликається автоматично, коли календар змінює дати (наприклад, перемикаєте місяць)
  const fetchLessons = async (info) => {
    try {
      // Запит до Python: Дай уроки від [дата_початку] до [дата_кінця]
      const response = await axios.get(`${API_URL}/lessons/`, {
        params: { 
          start: info.startStr, 
          end: info.endStr 
        }
      });
      
      // Перетворюємо дані у формат, зрозумілий календарю
      const calendarEvents = response.data.map(lesson => ({
        id: lesson.id,
        title: lesson.topic || 'Заняття',
        start: lesson.start_time,
        end: lesson.end_time,
        backgroundColor: lesson.status === 'planned' ? '#3B82F6' : '#10B981', // Синій або Зелений
        borderColor: 'transparent'
      }));

      setEvents(calendarEvents);
    } catch (error) {
      console.error("Помилка завантаження уроків:", error);
    }
  };

  return (
    <div className="h-[800px] bg-white p-4 rounded shadow">
      <FullCalendar
        plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
        initialView="timeGridWeek" // Починаємо з тижневого виду
        
        // Налаштування шапки
        headerToolbar={{
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek'
        }}
        
        // Локалізація та час
        firstDay={1} // Тиждень з понеділка
        locale="uk"  // Мова (якщо FullCalendar підтягне)
        slotMinTime="08:00:00" // Початок дня
        slotMaxTime="22:00:00" // Кінець дня
        allDaySlot={false} // Прибрати рядок "весь день"
        
        // Дані
        events={events}
        datesSet={fetchLessons} // Завантажувати нові дані при перемиканні
        
        // Інтерактивність (поки тільки перегляд)
        editable={true} 
      />
    </div>
  );
}
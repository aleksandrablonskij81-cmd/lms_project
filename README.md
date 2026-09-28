# LMS Project (Django REST Framework)

API для LMS-системы: пользователи, курсы, уроки.

## Технологии

- Python 3.14
- Django 6.1
- Django REST Framework
- PostgreSQL
- Pillow (для картинок)

## Установка

### 1. Клонировать репозиторий

```bash
git clone https://github.com/aleksandrablonskij81-cmd/lms_project.git
cd lms_project

---

## Тестирование API (Postman)

Все эндпоинты протестированы:

| # | Метод | URL | Статус |
|---|-------|-----|--------|
| 1 | GET | `/api/courses/` | 200 OK |
| 2 | POST | `/api/courses/` | 201 Created |
| 3 | GET | `/api/courses/1/` | 200 OK |
| 4 | PUT | `/api/courses/1/` | 200 OK |
| 5 | DELETE | `/api/courses/2/` | 204 No Content |
| 6 | GET | `/api/lessons/` | 200 OK |
| 7 | POST | `/api/lessons/` | 201 Created |
| 8 | GET | `/api/lessons/1/` | 200 OK |
| 9 | PUT | `/api/lessons/1/` | 200 OK |
| 10 | DELETE | `/api/lessons/2/` | 204 No Content |
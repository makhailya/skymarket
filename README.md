# 🛒 SkyMarket — Доска объявлений SB1

REST API для платформы объявлений. Пользователи могут 
публиковать объявления, оставлять отзывы и управлять своим профилем.

## 📋 Стек технологий

- **Python 3.13**
- **Django 6.0** + **Django REST Framework**
- **PostgreSQL 15**
- **JWT** авторизация (SimpleJWT + Djoser)
- **Docker** + **Docker Compose**
- **Poetry** — управление зависимостями
- **pytest** — тестирование (покрытие 78%+)

## 🚀 Быстрый старт

### Через Docker (рекомендуется)

1. Клонируй репозиторий:
```bash
   git clone https://github.com/твой-username/skymarket.git
   cd skymarket
```

2. Создай `.env` файл:
```bash
   cp .env.example .env
```

3. Запусти проект:
```bash
   docker-compose up --build
```

4. Создай суперпользователя:
```bash
   docker-compose exec web python manage.py createsuperuser
```

Проект доступен на `http://localhost:8000` ✅

---

### Без Docker (локально)

1. Установи зависимости:
```bash
   poetry install
   poetry shell
```

2. Примени миграции:
```bash
   python manage.py migrate
```

3. Запусти сервер:
```bash
   python manage.py runserver
```

## 📌 API Endpoints

### Авторизация
| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/auth/users/` | Регистрация |
| POST | `/auth/jwt/create/` | Получить токен |
| POST | `/auth/jwt/refresh/` | Обновить токен |

### Пользователи
| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/users/me/` | Мой профиль |
| PATCH | `/users/me/` | Обновить профиль |

### Объявления
| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/ads/` | Все объявления |
| POST | `/ads/` | Создать объявление |
| GET | `/ads/{id}/` | Одно объявление |
| PATCH | `/ads/{id}/` | Редактировать |
| DELETE | `/ads/{id}/` | Удалить |
| GET | `/ads/me/` | Мои объявления |

### Отзывы
| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/ads/{id}/reviews/` | Отзывы к объявлению |
| POST | `/ads/{id}/reviews/` | Написать отзыв |
| PATCH | `/ads/{id}/reviews/{id}/` | Редактировать отзыв |
| DELETE | `/ads/{id}/reviews/{id}/` | Удалить отзыв |

## 🔐 Права доступа

| Действие | Аноним | Пользователь | Администратор |
|----------|--------|--------------|---------------|
| Просмотр объявлений | ✅ | ✅ | ✅ |
| Создание объявления | ❌ | ✅ | ✅ |
| Редактирование своего | ❌ | ✅ | ✅ |
| Редактирование чужого | ❌ | ❌ | ✅ |
| Удаление своего | ❌ | ✅ | ✅ |
| Удаление чужого | ❌ | ❌ | ✅ |

## 🧪 Тестирование
```bash
# Запуск тестов
TESTING=1 poetry run pytest -v

# С отчётом о покрытии
TESTING=1 coverage run -m pytest
coverage report
```

## 🗂️ Структура проекта
```
skymarket/
├── config/          # Настройки Django
├── users/           # Приложение пользователей
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── ads/             # Объявления и отзывы
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   └── urls.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## 👤 Автор

**Маханек Илья** — [GitHub](https://github.com/makhailya)
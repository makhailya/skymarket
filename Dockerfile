# Берём официальный образ Python
FROM python:3.13-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем Poetry
RUN pip install poetry

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
# --no-root — не устанавливаем сам проект как пакет
# --no-dev — не устанавливаем dev зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

# Копируем весь проект
COPY . .

# Открываем порт 8000
EXPOSE 8000

# Команда запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

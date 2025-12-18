FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем зависимости
COPY pyproject.toml .
RUN uv sync

# Копируем код
COPY . .

# Создаем пользователя
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Команды по умолчанию будут переопределены в docker-compose
CMD ["gunicorn", "phone_lookup.wsgi:application", "--bind", "0.0.0.0:8000"]
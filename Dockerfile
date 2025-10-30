# Dockerfile для развертывания RAG системы на RunPod
FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование requirements.txt
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY src/ ./src/
COPY data/ ./data/
COPY config/ ./config/

# Копирование .env файла (если есть)
COPY .env* ./

# Создание директорий для данных
RUN mkdir -p /app/data/raw /app/data/processed

# Переменные окружения по умолчанию
ENV PYTHONUNBUFFERED=1
ENV MILVUS_HOST=localhost
ENV MILVUS_PORT=19530

# Expose порт для API (если будет использоваться)
EXPOSE 8000

# Команда запуска по умолчанию
CMD ["python", "-m", "src.main", "--help"]

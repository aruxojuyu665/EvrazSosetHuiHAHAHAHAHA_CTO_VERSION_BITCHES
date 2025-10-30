# Dockerfile для развертывания RAG системы на RunPod (CPU версия)
# Для GPU используйте Dockerfile.gpu
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

# Установка PyTorch CPU версии
RUN pip install --no-cache-dir torch==2.1.2 --index-url https://download.pytorch.org/whl/cpu

# Установка остальных Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Предзагрузка модели эмбеддингов (опционально)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('intfloat/multilingual-e5-large')" || true

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
ENV EMBEDDING_TYPE=local
ENV LOCAL_EMBEDDING_MODEL=intfloat/multilingual-e5-large
ENV LOCAL_EMBEDDING_DEVICE=cpu

# Expose порт для API (если будет использоваться)
EXPOSE 8000

# Команда запуска по умолчанию
CMD ["python", "-m", "src.main", "--help"]

#!/bin/bash
# Скрипт для запуска RAG системы на RunPod

set -e

echo "========================================="
echo "GOST RAG System - RunPod Startup"
echo "========================================="

# Проверка переменных окружения
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "ERROR: OPENROUTER_API_KEY не установлен"
    exit 1
fi

if [ -z "$EMBEDDING_API_KEY" ]; then
    echo "ERROR: EMBEDDING_API_KEY не установлен"
    exit 1
fi

# Установка зависимостей (если еще не установлены)
echo "Проверка зависимостей..."
pip install -q -r /app/requirements.txt

# Ожидание запуска Milvus
echo "Ожидание запуска Milvus..."
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if nc -z ${MILVUS_HOST:-localhost} ${MILVUS_PORT:-19530} 2>/dev/null; then
        echo "Milvus доступен!"
        break
    fi
    
    attempt=$((attempt + 1))
    echo "Попытка $attempt/$max_attempts..."
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo "ERROR: Не удалось подключиться к Milvus"
    exit 1
fi

# Проверка наличия данных
if [ ! -f "/app/data/raw/GOST_27772-2021.pdf" ]; then
    echo "WARNING: Файл GOST_27772-2021.pdf не найден в /app/data/raw/"
fi

echo "========================================="
echo "Система готова к работе!"
echo "========================================="
echo ""
echo "Доступные команды:"
echo "  python -m src.main index --input /app/data/raw --create-new"
echo "  python -m src.main extract --class-name C235"
echo "  python -m src.main query --question 'Ваш вопрос'"
echo "  python -m src.main stats"
echo ""

# Если передана команда, выполнить её
if [ $# -gt 0 ]; then
    echo "Выполнение команды: $@"
    exec "$@"
else
    # Иначе запустить интерактивную оболочку
    exec /bin/bash
fi

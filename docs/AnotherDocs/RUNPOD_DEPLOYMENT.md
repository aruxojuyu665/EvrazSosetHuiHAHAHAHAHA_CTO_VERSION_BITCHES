# Руководство по развертыванию на RunPod

Данное руководство описывает процесс развертывания RAG системы анализа ГОСТ на платформе RunPod.

## Предварительные требования

Перед началом убедитесь, что у вас есть:

- Аккаунт на [RunPod](https://www.runpod.io/)
- API ключ OpenRouter для доступа к Claude 3.5 Sonnet
- API ключ OpenAI для embeddings (или альтернативный провайдер)
- Docker Hub аккаунт (опционально, для загрузки собственного образа)

## Вариант 1: Использование Docker Compose (рекомендуется для локальной разработки)

### Шаг 1: Подготовка окружения

Создайте `.env` файл на основе `.env.example`:

```bash
cp .env.example .env
```

Заполните необходимые переменные:

```env
OPENROUTER_API_KEY=sk-or-v1-xxxxx
EMBEDDING_API_KEY=sk-xxxxx
MILVUS_HOST=milvus
MILVUS_PORT=19530
```

### Шаг 2: Запуск сервисов

```bash
docker-compose up -d
```

Это запустит:
- Milvus (векторная БД)
- etcd (для Milvus)
- MinIO (объектное хранилище для Milvus)
- RAG приложение

### Шаг 3: Проверка статуса

```bash
docker-compose ps
docker-compose logs rag-app
```

### Шаг 4: Индексирование документов

```bash
docker-compose exec rag-app python -m src.main index --input /app/data/raw --create-new
```

## Вариант 2: Развертывание на RunPod

### Шаг 1: Подготовка Docker образа

#### Опция A: Использование готового образа

Соберите и загрузите образ в Docker Hub:

```bash
# Сборка образа
docker build -t yourusername/gost-rag-system:latest .

# Вход в Docker Hub
docker login

# Загрузка образа
docker push yourusername/gost-rag-system:latest
```

#### Опция B: Использование GitHub Container Registry

```bash
# Вход в GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Тегирование образа
docker tag gost-rag-system ghcr.io/yourusername/gost-rag-system:latest

# Загрузка образа
docker push ghcr.io/yourusername/gost-rag-system:latest
```

### Шаг 2: Создание Pod на RunPod

1. Войдите в [RunPod Console](https://www.runpod.io/console/pods)

2. Нажмите **"+ Deploy"**

3. Выберите **"Deploy a Custom Container"**

4. Настройте параметры:

   **Container Configuration:**
   - **Container Image**: `yourusername/gost-rag-system:latest`
   - **Docker Command**: `/bin/bash /app/runpod_start.sh`
   - **Container Disk**: 20 GB (минимум)

   **Environment Variables:**
   ```
   OPENROUTER_API_KEY=sk-or-v1-xxxxx
   EMBEDDING_API_KEY=sk-xxxxx
   MILVUS_HOST=localhost
   MILVUS_PORT=19530
   ```

   **GPU Selection:**
   - Для embeddings и inference: RTX 3090 или выше (опционально)
   - Можно использовать CPU-only вариант

   **Volume Mounts:**
   - `/workspace/data` → `/app/data` (для персистентности данных)

5. Нажмите **"Deploy"**

### Шаг 3: Настройка Milvus

Для RunPod рекомендуется использовать внешний Milvus или запустить его в отдельном контейнере.

#### Опция A: Внешний Milvus (рекомендуется)

Используйте Milvus Cloud или разверните Milvus на отдельном сервере:

```env
MILVUS_HOST=your-milvus-instance.com
MILVUS_PORT=19530
```

#### Опция B: Milvus в том же Pod

Добавьте в `docker-compose.yml` или используйте RunPod Template с несколькими контейнерами.

### Шаг 4: Подключение к Pod

1. В RunPod Console найдите ваш Pod

2. Нажмите **"Connect"** → **"Start Web Terminal"** или используйте SSH

3. Проверьте статус:
```bash
python -m src.main stats
```

### Шаг 5: Индексирование документов

```bash
# Загрузите PDF файлы в /app/data/raw/
# Затем выполните индексирование
python -m src.main index --input /app/data/raw --create-new
```

### Шаг 6: Использование системы

```bash
# Извлечение информации о классе прочности
python -m src.main extract --class-name C235

# Произвольный запрос
python -m src.main query --question "Какие требования к химическому составу стали класса C235?"
```

## Вариант 3: Использование RunPod Serverless

Для serverless развертывания:

### Шаг 1: Создание Handler

Создайте `handler.py` для RunPod Serverless:

```python
import runpod
from src.rag import GOSTRAGSystem

# Инициализация RAG системы
rag_system = GOSTRAGSystem()
rag_system.initialize_milvus()
rag_system.load_index()
rag_system.setup_query_engine()

def handler(event):
    """Handler для RunPod Serverless"""
    question = event["input"]["question"]
    result = rag_system.query(question)
    return {"output": result}

runpod.serverless.start({"handler": handler})
```

### Шаг 2: Обновление Dockerfile

```dockerfile
# Добавьте в конец Dockerfile
COPY handler.py /app/
CMD ["python", "-u", "/app/handler.py"]
```

### Шаг 3: Развертывание

1. Загрузите образ в Docker Hub
2. В RunPod Console выберите **"Serverless"**
3. Создайте новый Endpoint с вашим образом

## Мониторинг и отладка

### Просмотр логов

```bash
# Docker Compose
docker-compose logs -f rag-app

# RunPod
# Используйте Web Terminal или SSH
tail -f /var/log/app.log
```

### Проверка подключения к Milvus

```bash
python -c "from pymilvus import connections; connections.connect('default', host='localhost', port=19530); print('Connected!')"
```

### Проверка использования памяти

```bash
# Статистика Milvus
python -m src.main stats

# Системная память
free -h
```

## Оптимизация производительности

### 1. Настройка chunk_size

Для больших документов увеличьте `CHUNK_SIZE`:

```env
CHUNK_SIZE=1500
CHUNK_OVERLAP=300
```

### 2. Настройка top_k

Для более точных результатов увеличьте `TOP_K_RESULTS`:

```env
TOP_K_RESULTS=10
```

### 3. Кэширование embeddings

Embeddings автоматически кэшируются в Milvus, но можно дополнительно настроить:

```python
# В config.py
cache_embeddings = True
```

## Устранение неполадок

### Проблема: Не удается подключиться к Milvus

**Решение:**
1. Проверьте, что Milvus запущен: `docker ps | grep milvus`
2. Проверьте переменные окружения: `echo $MILVUS_HOST`
3. Проверьте сетевое подключение: `nc -zv localhost 19530`

### Проблема: Ошибка API ключа

**Решение:**
1. Проверьте `.env` файл
2. Убедитесь, что ключи правильно экспортированы: `echo $OPENROUTER_API_KEY`
3. Проверьте квоты на OpenRouter/OpenAI

### Проблема: Недостаточно памяти

**Решение:**
1. Уменьшите `CHUNK_SIZE`
2. Уменьшите `TOP_K_RESULTS`
3. Увеличьте ресурсы Pod на RunPod

## Безопасность

### Защита API ключей

Никогда не коммитьте `.env` файл в Git:

```bash
# Убедитесь, что .env в .gitignore
echo ".env" >> .gitignore
```

### Использование RunPod Secrets

В RunPod можно использовать секреты вместо переменных окружения:

1. В RunPod Console → **Secrets**
2. Добавьте секреты
3. Ссылайтесь на них в конфигурации Pod

## Масштабирование

Для обработки большого количества запросов:

1. **Horizontal Scaling**: Создайте несколько Pod
2. **Load Balancer**: Используйте RunPod Load Balancer
3. **Shared Milvus**: Все Pod подключаются к одному Milvus instance

## Резервное копирование

### Backup Milvus данных

```bash
# Экспорт коллекции
python -c "from pymilvus import utility; utility.export_collection('gost_documents', '/backup/collection.json')"

# Копирование на S3 или другое хранилище
aws s3 cp /backup/collection.json s3://your-bucket/backups/
```

## Стоимость

Примерная стоимость на RunPod:

- **GPU Pod (RTX 3090)**: ~$0.40/час
- **CPU Pod**: ~$0.10/час
- **Serverless**: Pay per request

Для оптимизации затрат используйте Spot Instances.

## Дополнительные ресурсы

- [RunPod Documentation](https://docs.runpod.io/)
- [Milvus Documentation](https://milvus.io/docs)
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [OpenRouter API](https://openrouter.ai/docs)

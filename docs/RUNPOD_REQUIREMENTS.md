# Требования для развертывания на RunPod

## Обзор

Данный документ описывает минимальные и рекомендуемые требования для развертывания полного стека RAG системы на одном сервере RunPod.

## Архитектура развертывания

Система развертывается на одном сервере RunPod и включает следующие компоненты:

```
┌─────────────────────────────────────────────────────────────┐
│                      RunPod Instance                        │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                  Docker Containers                    │ │
│  │                                                       │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │ │
│  │  │   Milvus    │  │    etcd     │  │   MinIO     │  │ │
│  │  │ (Port 19530)│  │ (Port 2379) │  │ (Port 9000) │  │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  │ │
│  │                                                       │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │            RAG Application                      │ │ │
│  │  │         (Python 3.11)                           │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  External API Calls:                                        │
│  ├─ OpenRouter API (Claude 3.5 Sonnet)                     │
│  └─ OpenAI API (Embeddings)                                │
└─────────────────────────────────────────────────────────────┘
```

## Системные требования

### Минимальные требования

Для базовой работы с небольшими документами (1-5 PDF файлов):

#### CPU
- **Ядра:** 4 vCPU
- **Архитектура:** x86_64
- **Частота:** 2.5 GHz+

#### Память (RAM)
- **Минимум:** 16 GB
- **Распределение:**
  - Milvus: 4 GB
  - etcd: 1 GB
  - MinIO: 1 GB
  - RAG Application: 4 GB
  - System overhead: 2 GB
  - Buffer: 4 GB

#### Хранилище
- **Минимум:** 50 GB SSD
- **Распределение:**
  - OS + Docker: 10 GB
  - Milvus data: 10 GB
  - MinIO objects: 10 GB
  - PDF documents: 5 GB
  - Logs & temp: 5 GB
  - Buffer: 10 GB

#### Сеть
- **Пропускная способность:** 100 Mbps+
- **Исходящий трафик:** Неограниченный (для API вызовов)

### Рекомендуемые требования

Для production использования с большим объемом документов (10-50 PDF файлов):

#### CPU
- **Ядра:** 8 vCPU
- **Архитектура:** x86_64
- **Частота:** 3.0 GHz+

#### Память (RAM)
- **Рекомендуется:** 32 GB
- **Распределение:**
  - Milvus: 8 GB
  - etcd: 2 GB
  - MinIO: 2 GB
  - RAG Application: 8 GB
  - System overhead: 4 GB
  - Buffer: 8 GB

#### Хранилище
- **Рекомендуется:** 200 GB SSD
- **Тип:** NVMe SSD (предпочтительно)
- **Распределение:**
  - OS + Docker: 20 GB
  - Milvus data: 50 GB
  - MinIO objects: 50 GB
  - PDF documents: 30 GB
  - Logs & temp: 20 GB
  - Buffer: 30 GB

#### Сеть
- **Пропускная способность:** 1 Gbps+
- **Исходящий трафик:** Неограниченный

### Оптимальные требования

Для высоконагруженных систем с большим количеством документов (50+ PDF файлов):

#### CPU
- **Ядра:** 16 vCPU
- **Архитектура:** x86_64
- **Частота:** 3.5 GHz+

#### Память (RAM)
- **Оптимально:** 64 GB
- **Распределение:**
  - Milvus: 16 GB
  - etcd: 4 GB
  - MinIO: 4 GB
  - RAG Application: 16 GB
  - System overhead: 8 GB
  - Buffer: 16 GB

#### Хранилище
- **Оптимально:** 500 GB NVMe SSD
- **IOPS:** 10,000+
- **Распределение:**
  - OS + Docker: 30 GB
  - Milvus data: 150 GB
  - MinIO objects: 150 GB
  - PDF documents: 70 GB
  - Logs & temp: 50 GB
  - Buffer: 50 GB

## Требования к GPU

### Базовая конфигурация (без GPU)
Система может работать **без GPU**, так как:
- Embeddings генерируются через OpenAI API (облачно)
- LLM inference выполняется через OpenRouter API (облачно)
- Локальные вычисления минимальны

**Преимущества:**
- Более низкая стоимость
- Проще в настройке
- Достаточно для большинства случаев

### С GPU (опционально)

Если планируется использование локальных моделей в будущем:

#### Минимальные требования
- **GPU:** NVIDIA RTX 3060
- **VRAM:** 12 GB
- **CUDA:** 11.8+

#### Рекомендуемые требования
- **GPU:** NVIDIA RTX 3090 / A4000
- **VRAM:** 24 GB
- **CUDA:** 12.0+

#### Оптимальные требования
- **GPU:** NVIDIA A6000 / A100
- **VRAM:** 48 GB
- **CUDA:** 12.0+

**Примечание:** GPU требуется только при переходе на локальные модели для embeddings или LLM inference.

## Конфигурация RunPod Pod

### Выбор шаблона

#### Вариант 1: CPU-only (рекомендуется для начала)

**RunPod Template:**
- **Type:** CPU Pod
- **vCPU:** 8 cores
- **RAM:** 32 GB
- **Storage:** 200 GB SSD
- **Network:** 1 Gbps

**Примерная стоимость:** ~$0.10-0.15/час

#### Вариант 2: С GPU (для будущего расширения)

**RunPod Template:**
- **Type:** GPU Pod
- **GPU:** RTX 3090
- **vCPU:** 8 cores
- **RAM:** 32 GB
- **Storage:** 200 GB SSD
- **Network:** 1 Gbps

**Примерная стоимость:** ~$0.40-0.50/час

### Настройка Pod

#### Container Image
```
Docker Image: yourusername/gost-rag-system:latest
```

#### Environment Variables
```bash
# OpenRouter API
OPENROUTER_API_KEY=sk-or-v1-xxxxx
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet

# OpenAI Embeddings
EMBEDDING_API_KEY=sk-xxxxx
EMBEDDING_MODEL=text-embedding-3-small

# Milvus Configuration
MILVUS_HOST=localhost
MILVUS_PORT=19530
MILVUS_COLLECTION_NAME=gost_documents

# RAG Configuration
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
TEMPERATURE=0.1
MAX_TOKENS=4096
```

#### Volume Mounts
```bash
# Persistent storage for data
/workspace/data:/app/data

# Persistent storage for Milvus
/workspace/milvus:/var/lib/milvus

# Persistent storage for MinIO
/workspace/minio:/minio_data
```

#### Exposed Ports
```bash
# Milvus
19530:19530

# Milvus Web UI (optional)
9091:9091

# MinIO Console (optional)
9001:9001

# Future API (optional)
8000:8000
```

#### Docker Command
```bash
/bin/bash /app/runpod_start.sh
```

## Развертывание с Docker Compose

### Полная конфигурация на одном сервере

Используйте предоставленный `docker-compose.yml`:

```bash
# 1. Подключиться к RunPod Pod через SSH
ssh root@<pod-ip>

# 2. Клонировать репозиторий
git clone https://github.com/aruxojuyu665/EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES.git
cd EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES
git checkout RAG-Milvus-Manus-Edition

# 3. Настроить переменные окружения
cp .env.example .env
nano .env  # Добавить API ключи

# 4. Запустить все сервисы
docker-compose up -d

# 5. Проверить статус
docker-compose ps
docker-compose logs -f
```

### Проверка работоспособности

```bash
# Проверка Milvus
docker-compose exec milvus curl -X GET http://localhost:9091/healthz

# Проверка приложения
docker-compose exec rag-app python -m src.main stats

# Проверка подключения к API
docker-compose exec rag-app python -c "from src.config import config; config.validate_config()"
```

## Оценка ресурсов для различных сценариев

### Сценарий 1: Малый проект (1-5 документов)

**Документы:**
- 1-5 PDF файлов
- ~50-100 страниц каждый
- ~500 KB - 2 MB размер файла

**Ожидаемые метрики:**
- Векторов в Milvus: ~5,000 - 25,000
- Размер индекса: ~1-5 GB
- Время индексирования: 5-15 минут
- Время запроса: 2-5 секунд

**Требования:**
- CPU: 4 vCPU
- RAM: 16 GB
- Storage: 50 GB

### Сценарий 2: Средний проект (10-30 документов)

**Документы:**
- 10-30 PDF файлов
- ~50-200 страниц каждый
- ~500 KB - 5 MB размер файла

**Ожидаемые метрики:**
- Векторов в Milvus: ~50,000 - 150,000
- Размер индекса: ~10-30 GB
- Время индексирования: 30-60 минут
- Время запроса: 3-7 секунд

**Требования:**
- CPU: 8 vCPU
- RAM: 32 GB
- Storage: 200 GB

### Сценарий 3: Большой проект (50+ документов)

**Документы:**
- 50+ PDF файлов
- ~50-500 страниц каждый
- ~500 KB - 10 MB размер файла

**Ожидаемые метрики:**
- Векторов в Milvus: ~250,000 - 1,000,000
- Размер индекса: ~50-150 GB
- Время индексирования: 2-4 часа
- Время запроса: 5-10 секунд

**Требования:**
- CPU: 16 vCPU
- RAM: 64 GB
- Storage: 500 GB

## Оценка стоимости API

### OpenRouter API (Claude 3.5 Sonnet)

**Pricing:**
- Input: $3.00 / 1M tokens
- Output: $15.00 / 1M tokens

**Примерное использование:**
- Индексирование: минимальное (только metadata)
- Запрос: ~2,000 input tokens + ~1,000 output tokens
- Стоимость запроса: ~$0.021

**Месячная оценка (100 запросов/день):**
- 3,000 запросов/месяц
- Стоимость: ~$63/месяц

### OpenAI Embeddings API

**Pricing:**
- text-embedding-3-small: $0.02 / 1M tokens

**Примерное использование:**
- Индексирование 10 документов (~500 страниц): ~500,000 tokens
- Стоимость индексирования: ~$0.01
- Запросы: ~100 tokens/запрос
- Стоимость запросов (3,000/месяц): ~$0.006

**Месячная оценка:**
- Индексирование (разовое): ~$0.01
- Запросы: ~$0.006/месяц

### Общая стоимость

**Месячные затраты:**
- RunPod (CPU-only, 8 vCPU, 32GB RAM): ~$72-108/месяц (24/7)
- OpenRouter API: ~$63/месяц
- OpenAI Embeddings: ~$0.01/месяц
- **Итого: ~$135-171/месяц**

**Оптимизация затрат:**
- Использовать Spot Instances на RunPod (скидка до 50%)
- Останавливать Pod когда не используется
- Кэшировать частые запросы
- Batch обработка для индексирования

## Мониторинг ресурсов

### Команды для мониторинга

```bash
# CPU и память
docker stats

# Дисковое пространство
df -h

# Milvus статистика
docker-compose exec rag-app python -m src.main stats

# Логи
docker-compose logs -f --tail=100

# Сетевой трафик
iftop
```

### Метрики для отслеживания

1. **CPU Usage:** должно быть < 70% в среднем
2. **Memory Usage:** должно быть < 80%
3. **Disk I/O:** < 80% utilization
4. **Network:** < 50% bandwidth
5. **Milvus vectors:** количество индексированных векторов
6. **Query latency:** среднее время ответа

## Рекомендации по оптимизации

### 1. Для ограниченных ресурсов

```bash
# Уменьшить chunk_size
CHUNK_SIZE=500
CHUNK_OVERLAP=100

# Уменьшить top_k
TOP_K_RESULTS=3

# Ограничить max_tokens
MAX_TOKENS=2048
```

### 2. Для высокой производительности

```bash
# Увеличить chunk_size для лучшего контекста
CHUNK_SIZE=1500
CHUNK_OVERLAP=300

# Увеличить top_k для более точных результатов
TOP_K_RESULTS=10

# Больше токенов для развернутых ответов
MAX_TOKENS=8192
```

### 3. Для экономии API затрат

```bash
# Использовать меньше токенов
MAX_TOKENS=2048

# Меньше retrieval chunks
TOP_K_RESULTS=3

# Кэширование результатов (будущая функция)
ENABLE_CACHE=true
```

## Backup и восстановление

### Backup данных

```bash
# Backup Milvus data
docker-compose exec milvus tar -czf /backup/milvus-$(date +%Y%m%d).tar.gz /var/lib/milvus

# Backup MinIO data
docker-compose exec minio tar -czf /backup/minio-$(date +%Y%m%d).tar.gz /minio_data

# Backup PDF files
tar -czf backup-pdfs-$(date +%Y%m%d).tar.gz data/raw/
```

### Восстановление

```bash
# Restore Milvus data
docker-compose exec milvus tar -xzf /backup/milvus-YYYYMMDD.tar.gz -C /

# Restore MinIO data
docker-compose exec minio tar -xzf /backup/minio-YYYYMMDD.tar.gz -C /

# Restore PDF files
tar -xzf backup-pdfs-YYYYMMDD.tar.gz
```

## Troubleshooting

### Проблема: Недостаточно памяти

**Решение:**
1. Увеличить RAM инстанса
2. Уменьшить `CHUNK_SIZE` и `TOP_K_RESULTS`
3. Ограничить количество одновременных запросов

### Проблема: Медленные запросы

**Решение:**
1. Проверить CPU usage
2. Оптимизировать Milvus индекс
3. Уменьшить `TOP_K_RESULTS`
4. Использовать SSD вместо HDD

### Проблема: Ошибки API

**Решение:**
1. Проверить API ключи
2. Проверить квоты на OpenRouter/OpenAI
3. Проверить сетевое подключение
4. Добавить retry logic

## Заключение

Для успешного развертывания RAG системы на RunPod рекомендуется:

1. **Начать с минимальной конфигурации** (4 vCPU, 16 GB RAM, 50 GB SSD)
2. **Протестировать на малом наборе документов**
3. **Мониторить ресурсы** и масштабировать по необходимости
4. **Использовать CPU-only конфигурацию** (GPU не требуется)
5. **Настроить автоматический backup** для критичных данных

Система спроектирована для эффективной работы на одном сервере с возможностью горизонтального масштабирования в будущем.

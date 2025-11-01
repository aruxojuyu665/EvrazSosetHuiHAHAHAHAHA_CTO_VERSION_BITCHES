# Развертывание на RunPod с Milvus Lite

Эта инструкция описывает процесс развертывания проекта на сервере RunPod после миграции на Milvus Lite. **Docker больше не требуется для основного приложения.**

---

## Требования к серверу

| Компонент | Минимум | Рекомендуется |
|-----------|---------|---------------|
| **GPU** | RTX 3080 (10GB+) | RTX 3090 / A4000 (24GB+) |
| **CPU** | 8 vCPU | 12 vCPU |
| **RAM** | 30 GB | 60 GB |
| **Storage** | 100 GB SSD | 200 GB SSD |
| **OS** | Ubuntu 22.04 | Ubuntu 22.04 |

---

## Пошаговая инструкция

### 1. Подготовка сервера

Подключитесь к вашему серверу RunPod по SSH.

#### Обновление системы:

```bash
sudo apt update && sudo apt upgrade -y
```

#### Установка необходимых пакетов:

```bash
sudo apt install -y git python3.11 python3.11-venv
```

### 2. Клонирование репозитория

Клонируйте репозиторий и перейдите в ветку `milvus-lite-migration`:

```bash
git clone https://github.com/aruxojuyu665/EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES.git
cd EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES
git checkout milvus-lite-migration
```

### 3. Настройка проекта

#### Создание виртуального окружения:

```bash
python3.11 -m venv venv
source venv/bin/activate
```

#### Установка зависимостей:

```bash
pip install -r requirements.txt
```

#### Настройка `.env`:

```bash
cp .env.example .env
# Отредактируйте .env и добавьте ваш OPENROUTER_API_KEY
# Убедитесь, что LOCAL_EMBEDDING_DEVICE=cuda
```

### 4. Запуск и индексирование

#### Индексирование документов:

Запустите индексирование в фоновом режиме с помощью `nohup`:

```bash
nohup python -m src.main index --input data/raw --create-new &
```

Вы можете следить за процессом, просматривая лог-файл:

```bash
tail -f nohup.out
```

После завершения индексирования файл `milvus_lite.db` будет создан в корне проекта.

### 5. (Опционально) Запуск через FastAPI

Если вам нужен REST API, вы можете запустить приложение через FastAPI.

#### Установка FastAPI и Uvicorn (если не установлены):

```bash
pip install fastapi uvicorn
```

#### Запуск сервера:

Вам нужно будет создать файл `api/main.py` для запуска FastAPI. Пример:

```python
# api/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from src.rag import GOSTRAGSystem

app = FastAPI()
rag_system = GOSTRAGSystem()
rag_system.initialize_milvus()
rag_system.load_index()
rag_system.setup_query_engine()

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def query(request: QueryRequest):
    return rag_system.query(request.question)
```

Запустите сервер:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

---

## Заключение

Миграция на Milvus Lite значительно упрощает развертывание, устраняя необходимость в управлении Docker-контейнерами для векторной базы данных. Это снижает сложность и потенциальные точки отказа.

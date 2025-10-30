# Быстрый старт

Краткое руководство по запуску RAG системы для анализа документов ГОСТ.

## Предварительные требования

1. **API ключи:**
   - OpenRouter API ключ (для Claude 3.5 Sonnet)
   - OpenAI API ключ (для embeddings)

2. **Инфраструктура:**
   - RunPod инстанс или локальный сервер с Docker
   - Минимум: 4 vCPU, 16 GB RAM, 50 GB SSD

## Шаг 1: Клонирование репозитория

```bash
git clone https://github.com/aruxojuyu665/EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES.git
cd EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES
git checkout RAG-Milvus-Manus-Edition
```

## Шаг 2: Настройка переменных окружения

```bash
# Создать .env файл из шаблона
cp .env.example .env

# Отредактировать .env и добавить ваши API ключи
nano .env
```

**Обязательные переменные:**
```env
OPENROUTER_API_KEY=sk-or-v1-ваш_ключ
EMBEDDING_API_KEY=sk-ваш_ключ_openai
```

## Шаг 3: Запуск системы

### Вариант A: Docker Compose (рекомендуется)

```bash
# Запустить все сервисы
docker-compose up -d

# Проверить статус
docker-compose ps

# Просмотреть логи
docker-compose logs -f
```

### Вариант B: Локальная установка

```bash
# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt

# Запустить Milvus отдельно (требуется Docker)
docker-compose up -d milvus etcd minio
```

## Шаг 4: Индексирование документов

```bash
# С Docker Compose
docker-compose exec rag-app python -m src.main index \
  --input /app/data/raw/GOST_27772-2021.pdf \
  --create-new

# Локально
python -m src.main index \
  --input data/raw/GOST_27772-2021.pdf \
  --create-new
```

**Ожидаемое время:** 5-15 минут для одного документа (~100 страниц)

## Шаг 5: Извлечение информации

### Тестовая задача: Класс прочности C235

```bash
# С Docker Compose
docker-compose exec rag-app python -m src.main extract --class-name C235

# Локально
python -m src.main extract --class-name C235
```

**Результат:** Файл `data/processed/C235_info.json` с полной информацией о классе прочности.

### Произвольный запрос

```bash
# С Docker Compose
docker-compose exec rag-app python -m src.main query \
  --question "Какие требования к химическому составу стали класса C235?"

# Локально
python -m src.main query \
  --question "Какие требования к химическому составу стали класса C235?"
```

## Шаг 6: Просмотр статистики

```bash
# С Docker Compose
docker-compose exec rag-app python -m src.main stats

# Локально
python -m src.main stats
```

**Вывод:**
```json
{
  "milvus": {
    "name": "gost_documents",
    "num_entities": 1234,
    "description": "GOST documents collection"
  },
  "config": {
    "model": "anthropic/claude-3.5-sonnet",
    "embedding_model": "text-embedding-3-small",
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "top_k": 5
  }
}
```

## Команды CLI

### index - Индексирование документов
```bash
python -m src.main index --input <path> [--create-new]
```
- `--input`: Путь к PDF файлу или директории
- `--create-new`: Создать новый индекс (удалит существующий)

### extract - Извлечение информации о классе прочности
```bash
python -m src.main extract --class-name <name> [--output <file>]
```
- `--class-name`: Название класса прочности (например, C235)
- `--output`: Файл для сохранения результата (опционально)

### query - Произвольный запрос
```bash
python -m src.main query --question "<question>" [--output <file>]
```
- `--question`: Вопрос к системе
- `--output`: Файл для сохранения результата (опционально)

### stats - Статистика системы
```bash
python -m src.main stats
```

## Проверка работоспособности

### 1. Проверка Milvus
```bash
docker-compose exec milvus curl -X GET http://localhost:9091/healthz
```

### 2. Проверка подключения к API
```bash
docker-compose exec rag-app python -c "from src.config import config; config.validate_config()"
```

### 3. Проверка индекса
```bash
docker-compose exec rag-app python -m src.main stats
```

## Остановка системы

```bash
# Остановить все сервисы
docker-compose down

# Остановить и удалить данные
docker-compose down -v
```

## Troubleshooting

### Проблема: "OPENROUTER_API_KEY не установлен"
**Решение:** Проверьте файл `.env` и убедитесь, что ключи правильно указаны.

### Проблема: "Не удалось подключиться к Milvus"
**Решение:** 
```bash
# Проверить статус Milvus
docker-compose ps milvus

# Перезапустить Milvus
docker-compose restart milvus
```

### Проблема: Медленная индексация
**Решение:** Это нормально для больших документов. Ожидайте ~1-2 минуты на 10 страниц.

### Проблема: Ошибка API rate limit
**Решение:** Подождите несколько минут и повторите запрос. Проверьте квоты на OpenRouter/OpenAI.

## Следующие шаги

1. **Добавьте больше документов:**
   ```bash
   python -m src.main index --input data/raw/
   ```

2. **Экспериментируйте с запросами:**
   - Попробуйте разные вопросы
   - Извлеките информацию о других классах прочности

3. **Настройте параметры:**
   - Измените `CHUNK_SIZE` и `TOP_K_RESULTS` в `.env`
   - Перезапустите систему для применения изменений

4. **Изучите документацию:**
   - [Архитектура системы](docs/SYSTEM_ARCHITECTURE.md)
   - [Требования RunPod](docs/RUNPOD_REQUIREMENTS.md)
   - [Развертывание на RunPod](docs/RUNPOD_DEPLOYMENT.md)

## Полезные ссылки

- **GitHub:** https://github.com/aruxojuyu665/EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES
- **Ветка:** RAG-Milvus-Manus-Edition
- **Документация:** [docs/](docs/)

## Поддержка

При возникновении проблем:
1. Проверьте логи: `docker-compose logs -f`
2. Изучите документацию в `docs/`
3. Создайте issue на GitHub

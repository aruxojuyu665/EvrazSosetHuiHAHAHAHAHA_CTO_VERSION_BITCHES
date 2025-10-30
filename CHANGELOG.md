# Changelog

Все значимые изменения в проекте будут документированы в этом файле.

## [0.2.0] - 2025-10-30 - RAG System Implementation

### Добавлено
- **RAG система** на основе LlamaIndex с интеграцией OpenRouter API (Claude 3.5 Sonnet)
- **Milvus векторная БД** для хранения и поиска embeddings
- **Модуль конфигурации** (`src/config.py`) с поддержкой переменных окружения
- **Milvus менеджер** (`src/vector_store/milvus_store.py`) для управления векторной БД
- **RAG система** (`src/rag/rag_system.py`) с полным функционалом:
  - Индексирование документов
  - Векторный поиск
  - Генерация ответов с использованием Claude 3.5 Sonnet
  - Извлечение информации о классах прочности
- **CLI интерфейс** в `src/main.py` с командами:
  - `index` - индексирование документов
  - `query` - выполнение запросов
  - `extract` - извлечение информации о классе прочности
  - `stats` - статистика системы
- **Docker конфигурация**:
  - `Dockerfile` для сборки образа
  - `docker-compose.yml` для локальной разработки с Milvus
  - `runpod_start.sh` - скрипт запуска на RunPod
  - `.dockerignore` для оптимизации образа
- **Тесты**:
  - `tests/test_rag_system.py` - тесты RAG системы
  - `tests/test_milvus_manager.py` - тесты Milvus менеджера
- **Документация**:
  - Обновлен `README.md` с полными инструкциями
  - `docs/RUNPOD_DEPLOYMENT.md` - руководство по развертыванию на RunPod
- **Конфигурационные файлы**:
  - `.env.example` - пример переменных окружения
  - Обновлен `requirements.txt` с зависимостями для RAG

### Изменено
- Обновлена структура проекта для поддержки RAG системы
- Расширен `src/main.py` с полноценным CLI интерфейсом
- Обновлен `README.md` с инструкциями по использованию RAG системы

### Технический стек
- Python 3.11
- LlamaIndex 0.9.48
- Milvus 2.3.7
- OpenRouter API (Claude 3.5 Sonnet)
- OpenAI Embeddings (text-embedding-3-small)
- Docker & Docker Compose
- FastAPI (для будущего API)

## [0.1.0] - 2025-10-30

### Добавлено
- Инициализация проекта
- Базовая структура репозитория
- Документация проекта (ТЗ, транскрипт встречи)
- Исходный файл ГОСТ 27772-2021
- Базовые модули:
  - `src/parsers/pdf_parser.py` - парсинг PDF документов
  - `src/extractors/data_extractor.py` - извлечение данных
  - `src/models/strength_class.py` - модели данных
- Конфигурационные файлы
- Базовая структура тестов
- Пример Jupyter notebook для исследовательского анализа
- README с описанием проекта
- requirements.txt с зависимостями

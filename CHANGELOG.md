# Changelog

Все значимые изменения в проекте будут документированы в этом файле.

## [0.4.0] - 2025-11-01 - Web Interface & Milvus Lite Migration

### Добавлено
- 🆕 **Веб-интерфейс** для RAG системы:
  - **Frontend:** React 19, TypeScript, Tailwind CSS, shadcn/ui
  - **Backend:** Node.js, Express, tRPC
  - **Функциональность:**
    - Семантический поиск по документам
    - Извлечение информации о классе прочности
    - Dashboard со статистикой системы
- 🆕 **FastAPI сервер** (`src/main.py api`) для интеграции с веб-интерфейсом
- 🆕 **Новая документация:**
  - `STRUCTURE.md` - полная структура проекта
  - `web/README.md` - документация по веб-интерфейсу

### Изменено
- **Миграция на Milvus Lite:**
  - Полностью удалена зависимость от Docker для Milvus
  - Обновлен `src/vector_store/milvus_store.py` для работы с `MilvusClient`
  - Обновлена конфигурация (`.env`) для использования `MILVUS_URI`
- **Обновлены зависимости:**
  - `pymilvus[milvus_lite]>=2.4.2`
  - `llama-index==0.10.68`
  - `torch>=2.1.0`
  - `transformers>=4.37.0`
- **Обновлена документация:**
  - `README.md` - полностью переписан с учетом веб-интерфейса
  - `QUICKSTART_LITE.md` - обновлен с инструкциями по запуску веб-интерфейса

### Исправлено
- Множественные проблемы совместимости версий `llama-index`
- Проблема с `context_window` для OpenRouter моделей
- Ошибка аутентификации OpenRouter
- Проблема с размерностью векторов для `text-embedding-3-large`

## [0.3.1] - 2025-10-31

### Added
- Comprehensive technical stack documentation (`docs/tech_stack.md`)
- Milvus Lite vs Standalone comparison (`docs/milvus_comparison.md`)
- RunPod deployment complete report (`docs/runpod_deployment_complete.md`)
- Deployment summary with problem analysis (`docs/deployment_summary.md`)

### Changed
- Updated deployment strategy to Milvus Lite (Docker-in-Docker issues on RunPod)
- Improved documentation structure

### Infrastructure
- Docker 28.5.1 installed on RunPod
- Python 3.11.14 environment configured
- All dependencies installed (~3.5 GB)
- GPU acceleration verified (RTX 3090)

### Notes
- Milvus Standalone requires Docker-in-Docker (not available on RunPod)
- Milvus Lite recommended for current deployment
- Code adaptation required for Milvus Lite integration

## [0.3.0] - 2025-10-30 - Local Embeddings & GPU Support

### Добавлено
- 🆕 **Поддержка локальных embedding моделей** (HuggingFace)
- Модель по умолчанию: `intfloat/multilingual-e5-large` (2.24 GB, 1024 dim)
- Поддержка GPU (CUDA 12.1+) для ускорения эмбеддингов

## [0.2.2] - 2025-10-30 - Testing & Deployment

### Добавлено
- **Комплексное тестирование:**
  - `tests/test_utils.py` - 10 тестов для retry декоратора
  - `tests/test_milvus_extended.py` - расширенные тесты Milvus
  - `tests/test_integration.py` - интеграционные тесты

## [0.2.1] - 2025-10-30 - Code Review Fixes

### Исправлено
- **P1-1:** Добавлена обработка ошибок при конвертации типов в config.py
- **P1-2:** Добавлена проверка подключения к Milvus перед операциями
- **P1-3:** Реализован context manager для MilvusManager

## [0.2.0] - 2025-10-30 - RAG System Implementation

### Добавлено
- **RAG система** на основе LlamaIndex с интеграцией OpenRouter API
- **Milvus векторная БД** для хранения и поиска embeddings
- **CLI интерфейс** в `src/main.py`

## [0.1.0] - 2025-10-30

### Добавлено
- Инициализация проекта
- Базовая структура репозитория
- Документация проекта

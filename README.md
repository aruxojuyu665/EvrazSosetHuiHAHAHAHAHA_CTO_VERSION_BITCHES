# ГОСТ Анализатор: RAG система для извлечения данных из стандартов

[![Tests](https://img.shields.io/badge/tests-19%20passed-brightgreen)](TESTING_REPORT.md)
[![Coverage](https://img.shields.io/badge/coverage-100%25%20(tested%20modules)-brightgreen)](TESTING_REPORT.md)
[![Version](https://img.shields.io/badge/version-0.4.0-blue)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.11-blue)](requirements.txt)

Проект для автоматического анализа и извлечения структурированных данных из документов стандартов ГОСТ с использованием RAG (Retrieval-Augmented Generation) подхода. **Эта версия использует Milvus Lite для упрощенного развертывания без Docker.**

---

## 📋 Описание проекта

Система предназначена для автоматизации процесса сбора и структурирования технической информации из стандартов ГОСТ. Основная задача — извлечение данных о классах прочности стали, их химическом составе, механических свойствах и других характеристиках, а также выявление взаимосвязей между различными стандартами.

### Ключевые возможности

✅ **Индексирование PDF документов** - автоматическая обработка и векторизация
✅ **Семантический поиск** - поиск релевантной информации по запросу
✅ **Извлечение структурированных данных** - автоматическое извлечение характеристик классов прочности
✅ **Анализ взаимосвязей** - выявление ссылок между стандартами
✅ **Локальные эмбеддинги** - поддержка GPU, нулевая стоимость API, приватность
🆕 **Milvus Lite** - упрощенное развертывание, не требует Docker
✅ **REST API** (планируется) - программный доступ к системе

---

## 🏗️ Архитектура

Система построена на следующих компонентах:

| Компонент | Технология | Назначение |
|-----------|------------|------------|
| **LLM** | Claude 3.5 Sonnet (OpenRouter) | Генерация ответов и анализ |
| **Embeddings** | Локальные (multilingual-e5-large) или OpenAI | Векторизация текста |
| **Vector Database** | 🆕 **Milvus Lite 2.3.5** | Хранение и поиск векторов (встроенная) |
| **RAG Framework** | LlamaIndex 0.9.48 | Оркестрация RAG pipeline |
| **PDF Processing** | PyPDF2, pdfplumber | Извлечение текста из PDF |
| **GPU Support** | ✅ CUDA 12.1+ (optional) | Ускорение эмбеддингов |
| **Deployment** | Локально или на сервере (без Docker) | Упрощенное развертывание |

**Подробнее:** [Архитектура системы](docs/SYSTEM_ARCHITECTURE.md)

---

## 🚀 Быстрый старт (с Milvus Lite)

Миграция на Milvus Lite значительно упростила установку. Теперь не требуется Docker для запуска векторной базы данных.

```bash
# 1. Клонировать репозиторий и перейти в нужную ветку
git clone https://github.com/aruxojuyu665/EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES.git
cd EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES
git checkout milvus-lite-migration

# 2. Создать виртуальное окружение
python3.11 -m venv venv
source venv/bin/activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Настроить переменные окружения
cp .env.example .env
# Отредактируйте .env и добавьте ваш OPENROUTER_API_KEY

# 5. Индексировать документы
# Milvus Lite автоматически создаст файл базы данных (milvus_lite.db)
python -m src.main index --input data/raw/GOST_27772-2021.pdf --create-new

# 6. Извлечь информацию о классе прочности C235
python -m src.main extract --class-name C235
```

**Подробнее:** [QUICKSTART_LITE.md](docs/QUICKSTART_LITE.md)

---

## 📖 Использование

### CLI команды

Система предоставляет 4 основные команды:

#### 1. `index` - Индексирование документов
```bash
python -m src.main index --input <path> [--create-new]
```
- `--input` - путь к PDF файлу или директории
- `--create-new` - создать новый индекс (удалит существующий)

#### 2. `extract` - Извлечение информации о классе прочности
```bash
python -m src.main extract --class-name <name> [--output <file>]
```
- `--class-name` - название класса прочности (по умолчанию: C235)
- `--output` - файл для сохранения результата (опционально)

#### 3. `query` - Произвольный запрос
```bash
python -m src.main query --question "<вопрос>" [--output <file>]
```
- `--question` - вопрос к системе
- `--output` - файл для сохранения результата (опционально)

#### 4. `stats` - Статистика системы
```bash
python -m src.main stats
```
Показывает статистику по коллекции Milvus Lite.

---

## ⚙️ Конфигурация (Milvus Lite)

Основные параметры настраиваются через переменные окружения в `.env`. Обратите внимание на новый параметр `MILVUS_URI`.

```env
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet

# Embedding Configuration
EMBEDDING_TYPE=local
LOCAL_EMBEDDING_MODEL=intfloat/multilingual-e5-large
LOCAL_EMBEDDING_DEVICE=cuda

# Milvus Lite Configuration
# URI - путь к файлу базы данных Milvus Lite
MILVUS_URI=./milvus_lite.db
MILVUS_COLLECTION_NAME=gost_documents
MILVUS_DIMENSION=1024
MILVUS_METRIC_TYPE=COSINE

# Deprecated: старые параметры для Milvus Standalone (не используются)
# MILVUS_HOST=localhost
# MILVUS_PORT=19530

# Application Settings
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
```

---

## 🌐 Развертывание на RunPod (с Milvus Lite)

Развертывание на RunPod также упрощено. Docker больше не является обязательным для работы приложения.

**📘 [План развертывания с Milvus Lite](docs/RUNPOD_DEPLOYMENT_LITE.md)**

---

## 📚 Документация

### Основная документация

- **[Быстрый старт (Milvus Lite)](docs/QUICKSTART_LITE.md)** - новое руководство по запуску
- **[Архитектура системы](docs/SYSTEM_ARCHITECTURE.md)** - логика работы и компоненты
- **[Отчет Code Review (Milvus Lite)](CODE_REVIEW_MILVUS_LITE.md)** - анализ изменений
- **[План миграции на Milvus Lite](docs/MILVUS_LITE_MIGRATION.md)** - исходный план

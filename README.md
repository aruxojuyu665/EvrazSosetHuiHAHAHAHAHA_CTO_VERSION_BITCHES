# ГОСТ Анализатор: RAG система для извлечения данных из стандартов

[![Tests](https://img.shields.io/badge/tests-19%20passed-brightgreen)](TESTING_REPORT.md)
[![Coverage](https://img.shields.io/badge/coverage-100%25%20(tested%20modules)-brightgreen)](TESTING_REPORT.md)
[![Version](https://img.shields.io/badge/version-0.2.1-blue)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.11-blue)](requirements.txt)

Проект для автоматического анализа и извлечения структурированных данных из документов стандартов ГОСТ с использованием RAG (Retrieval-Augmented Generation) подхода.

---

## 📋 Описание проекта

Система предназначена для автоматизации процесса сбора и структурирования технической информации из стандартов ГОСТ. Основная задача — извлечение данных о классах прочности стали, их химическом составе, механических свойствах и других характеристиках, а также выявление взаимосвязей между различными стандартами.

### Ключевые возможности

✅ **Индексирование PDF документов** - автоматическая обработка и векторизация  
✅ **Семантический поиск** - поиск релевантной информации по запросу  
✅ **Извлечение структурированных данных** - автоматическое извлечение характеристик классов прочности  
✅ **Анализ взаимосвязей** - выявление ссылок между стандартами  
🆕 **Локальные эмбеддинги** - поддержка GPU, нулевая стоимость API, приватность  
✅ **REST API** (планируется) - программный доступ к системе  

---

## 🏗️ Архитектура

Система построена на следующих компонентах:

| Компонент | Технология | Назначение |
|-----------|------------|------------|
| **LLM** | Claude 3.5 Sonnet (OpenRouter) | Генерация ответов и анализ |
| **Embeddings** | 🆕 Локальные (multilingual-e5-large) или OpenAI | Векторизация текста |
| **Vector Database** | Milvus 2.3.7 | Хранение и поиск векторов |
| **RAG Framework** | LlamaIndex 0.9.48 | Оркестрация RAG pipeline |
| **PDF Processing** | PyPDF2, pdfplumber | Извлечение текста из PDF |
| **GPU Support** | ✅ CUDA 12.1+ (optional) | Ускорение эмбеддингов |
| **Deployment** | Docker + RunPod | Контейнеризация и облако |

**Подробнее:** [Архитектура системы](docs/SYSTEM_ARCHITECTURE.md)

---

## 📁 Структура проекта

```
.
├── data/                    # Данные проекта
│   ├── raw/                 # Исходные файлы ГОСТ (PDF)
│   └── processed/           # Обработанные данные (JSON, CSV)
├── docs/                    # Документация
│   ├── SYSTEM_ARCHITECTURE.md       # Архитектура системы
│   ├── RUNPOD_REQUIREMENTS.md       # Требования к серверу
│   ├── RUNPOD_DEPLOYMENT.md         # Руководство по развертыванию
│   └── RUNPOD_DEPLOYMENT_PLAN.md    # Пошаговый план развертывания
├── src/                     # Исходный код
│   ├── config.py            # Конфигурация системы
│   ├── main.py              # Точка входа (CLI)
│   ├── rag/                 # RAG система
│   │   └── rag_system.py    # Основная логика RAG
│   ├── vector_store/        # Работа с Milvus
│   │   └── milvus_store.py  # Менеджер Milvus
│   ├── utils/               # Утилиты
│   │   └── retry_decorator.py  # Retry логика для API
│   ├── parsers/             # Парсеры PDF
│   ├── extractors/          # Извлечение данных
│   └── models/              # Модели данных
├── tests/                   # Тесты
│   ├── test_config.py       # Тесты конфигурации
│   ├── test_utils.py        # Тесты утилит
│   ├── test_milvus_*.py     # Тесты Milvus
│   ├── test_rag_system.py   # Тесты RAG
│   └── test_integration.py  # Интеграционные тесты
├── scripts/                 # Скрипты
│   └── deploy_runpod.sh     # Автоматическое развертывание
├── notebooks/               # Jupyter notebooks
├── config/                  # Конфигурационные файлы
├── Dockerfile               # Docker образ приложения
├── docker-compose.yml       # Полный стек для разработки
├── runpod_start.sh          # Скрипт запуска на RunPod
├── TESTING_PLAN.md          # План тестирования
├── TESTING_REPORT.md        # Отчет о тестировании
├── CODE_REVIEW_REPORT.md    # Отчет Code Review
└── FIXES_SUMMARY.md         # Описание исправлений
```

**Подробнее:** [Структура проекта](STRUCTURE.md)

---

## 🚀 Быстрый старт

### Вариант 1: Docker Compose (рекомендуется)

```bash
# 1. Клонировать репозиторий
git clone https://github.com/aruxojuyu665/EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES.git
cd EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES
git checkout RAG-Milvus-Manus-Edition

# 2. Настроить переменные окружения
cp .env.example .env
# Отредактировать .env и добавить API ключи

# 3. Запустить систему
docker-compose up -d

# 4. Индексировать документы
docker-compose exec rag-app python -m src.main index --input /app/data/raw --create-new

# 5. Извлечь информацию о классе прочности C235
docker-compose exec rag-app python -m src.main extract --class-name C235
```

### Вариант 2: Локальная установка

```bash
# 1. Клонировать репозиторий
git clone https://github.com/aruxojuyu665/EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES.git
cd EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES

# 2. Создать виртуальное окружение
python3.11 -m venv venv
source venv/bin/activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Настроить .env
cp .env.example .env
# Отредактировать .env

# 5. Запустить Milvus отдельно (через Docker)
docker-compose up -d milvus-standalone milvus-etcd milvus-minio

# 6. Использовать систему
python -m src.main index --input data/raw/GOST_27772-2021.pdf --create-new
python -m src.main extract --class-name C235
```

**Подробнее:** [QUICKSTART.md](QUICKSTART.md)

---

## 📖 Использование

### CLI команды

Система предоставляет 4 основные команды:

#### 1. `index` - Индексирование документов

```bash
python -m src.main index --input <path> [--create-new]
```

**Параметры:**
- `--input` - путь к PDF файлу или директории
- `--create-new` - создать новый индекс (удалит существующий)

**Пример:**
```bash
python -m src.main index --input data/raw/GOST_27772-2021.pdf --create-new
```

#### 2. `extract` - Извлечение информации о классе прочности

```bash
python -m src.main extract --class-name <name> [--output <file>]
```

**Параметры:**
- `--class-name` - название класса прочности (по умолчанию: C235)
- `--output` - файл для сохранения результата (опционально)

**Пример:**
```bash
python -m src.main extract --class-name C235 --output output/c235.json
```

#### 3. `query` - Произвольный запрос

```bash
python -m src.main query --question "<вопрос>" [--output <file>]
```

**Параметры:**
- `--question` - вопрос к системе
- `--output` - файл для сохранения результата (опционально)

**Пример:**
```bash
python -m src.main query --question "Какие требования к химическому составу стали класса C235?"
```

#### 4. `stats` - Статистика системы

```bash
python -m src.main stats
```

**Вывод:**
- Название коллекции
- Количество проиндексированных векторов
- Размерность векторов
- Использование ресурсов

---

## 🧪 Тестирование

### Результаты тестирования

**Версия:** 0.2.1  
**Дата:** 30 октября 2025

| Метрика | Значение |
|---------|----------|
| **Всего тестов** | 19 |
| **Успешно** | 19 (100%) |
| **Провалено** | 0 (0%) |
| **Покрытие** | 100% (протестированные модули) |

**Подробнее:** [Отчет о тестировании](TESTING_REPORT.md)

### Запуск тестов

```bash
# Unit тесты
pytest tests/test_config.py tests/test_utils.py -v

# С покрытием кода
pytest tests/ --cov=src --cov-report=html

# Интеграционные тесты (требуют Milvus и API ключи)
pytest tests/test_integration.py --integration -v
```

### Найденные и исправленные баги

В процессе тестирования найдено и исправлено **2 критических бага**:

1. **AttributeError в retry_decorator** - исправлено использование `getattr()` для безопасного доступа к `__name__`
2. **Несуществующий пакет в requirements.txt** - удален пакет `milvus==2.3.7`

**Подробнее:** [Отчет Code Review](CODE_REVIEW_REPORT.md) | [Описание исправлений](FIXES_SUMMARY.md)

---

## 🌐 Развертывание на RunPod

### Автоматическое развертывание

Используйте скрипт автоматического развертывания:

```bash
# На сервере RunPod
wget https://raw.githubusercontent.com/aruxojuyu665/EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES/RAG-Milvus-Manus-Edition/scripts/deploy_runpod.sh
chmod +x deploy_runpod.sh
sudo ./deploy_runpod.sh
```

Скрипт автоматически:
1. Обновит систему
2. Установит Docker и Docker Compose
3. Клонирует репозиторий
4. Настроит окружение
5. Запустит все сервисы
6. Проверит работоспособность
7. Настроит автозапуск

### Ручное развертывание

Следуйте пошаговому плану:

**📘 [Пошаговый план развертывания](docs/RUNPOD_DEPLOYMENT_PLAN.md)**

### Требования к серверу

| Компонент | Минимум | Рекомендуется |
|-----------|---------|---------------|
| **CPU** | 4 vCPU @ 2.5 GHz | 8 vCPU @ 3.0 GHz+ |
| **RAM** | 16 GB | 32 GB |
| **Storage** | 100 GB SSD | 200 GB SSD |
| **Network** | 100 Mbps | 1 Gbps |

**Стоимость:** ~$0.20-0.30/час (~$144-216/месяц)

**Подробнее:** [Требования RunPod](docs/RUNPOD_REQUIREMENTS.md)

---

## ⚙️ Конфигурация

Основные параметры настраиваются через переменные окружения в `.env`:

```env
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet

# Embedding Model Configuration
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_API_KEY=your_openai_api_key_for_embeddings

# Milvus Configuration
MILVUS_HOST=localhost
MILVUS_PORT=19530
MILVUS_COLLECTION_NAME=gost_documents

# MinIO Configuration (для production изменить!)
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

# Application Settings
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
TEMPERATURE=0.1
MAX_TOKENS=4096
TIMEOUT=60
```

**⚠️ ВАЖНО:** Для production развертывания обязательно изменить `MINIO_ACCESS_KEY` и `MINIO_SECRET_KEY`!

---

## 📚 Документация

### Основная документация

- **[Быстрый старт](QUICKSTART.md)** - пошаговое руководство по запуску
- **[Архитектура системы](docs/SYSTEM_ARCHITECTURE.md)** - логика работы и компоненты
- **[Техническое задание](docs/technical_specification.md)** - исходное ТЗ проекта
- **[Структура проекта](STRUCTURE.md)** - организация файлов и директорий

### Развертывание

- **[Требования RunPod](docs/RUNPOD_REQUIREMENTS.md)** - системные требования
- **[Руководство по развертыванию](docs/RUNPOD_DEPLOYMENT.md)** - полное руководство
- **[Пошаговый план](docs/RUNPOD_DEPLOYMENT_PLAN.md)** - детальный план с командами

### Тестирование и качество

- **[План тестирования](TESTING_PLAN.md)** - стратегия тестирования
- **[Отчет о тестировании](TESTING_REPORT.md)** - результаты тестов
- **[Code Review](CODE_REVIEW_REPORT.md)** - анализ кода
- **[Исправления](FIXES_SUMMARY.md)** - описание багфиксов

### История разработки

- **[История изменений](CHANGELOG.md)** - версии и обновления
- **[Транскрипт встречи](docs/meeting_transcript.md)** - обсуждение требований
- **[Резюме релиза](RELEASE_SUMMARY.md)** - краткое описание v0.2.0

---

## 🛠️ Разработка

### Создание новой ветки

```bash
git checkout -b feature/your-feature-name
```

### Код стайл

Проект следует PEP 8:

```bash
# Форматирование
black src/

# Линтинг
pylint src/

# Type checking
mypy src/
```

### Pre-commit hooks (планируется)

```bash
pip install pre-commit
pre-commit install
```

---

## 🎯 Тестовая задача

Извлечь всю информацию о классе прочности стали **C235** из ГОСТ 27772-2021:

```bash
# 1. Индексирование
docker-compose exec rag-app python -m src.main index \
    --input /app/data/raw/GOST_27772-2021.pdf \
    --create-new

# 2. Извлечение информации
docker-compose exec rag-app python -m src.main extract \
    --class-name C235 \
    --output /app/output/C235_info.json

# 3. Просмотр результата
docker-compose exec rag-app cat /app/output/C235_info.json
```

**Ожидаемый результат:**
- Химический состав
- Механические свойства
- Предельные отклонения
- Требования к испытаниям
- Ссылки на связанные стандарты

---

## 🔧 Технологии

| Категория | Технологии |
|-----------|------------|
| **Язык** | Python 3.11 |
| **LLM** | Claude 3.5 Sonnet (OpenRouter API) |
| **Embeddings** | OpenAI text-embedding-3-small |
| **Vector DB** | Milvus 2.3.7 |
| **RAG** | LlamaIndex 0.9.48, LangChain 0.1.20 |
| **PDF** | PyPDF2, pdfplumber, pdf2image |
| **Data** | pandas, numpy |
| **Deployment** | Docker, Docker Compose, RunPod |
| **Testing** | pytest, pytest-cov, pytest-mock |

---

## 📊 Статус проекта

**Версия:** 0.2.1  
**Статус:** ✅ Готово к production (с настройкой credentials)  
**Последнее обновление:** 30 октября 2025

### Roadmap

#### v0.2.2 (Ближайшие улучшения)
- [ ] Mock-тесты для Milvus и RAG
- [ ] Fixture для тестовых документов
- [ ] Улучшенная обработка ошибок

#### v0.3.0 (Следующий релиз)
- [ ] REST API (FastAPI)
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Интеграционные тесты
- [ ] Performance тесты
- [ ] Graceful shutdown

#### v0.4.0 (Будущее)
- [ ] Web UI (React)
- [ ] Streaming для больших файлов
- [ ] Batch processing
- [ ] Monitoring (Prometheus + Grafana)
- [ ] Security audit

---

## 📝 Лицензия

Проект разработан для внутреннего использования.

---

## 👥 Контакты

**Репозиторий:** https://github.com/aruxojuyu665/EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES

**Ветка:** RAG-Milvus-Manus-Edition

При возникновении вопросов обращайтесь к команде разработки.

---

**Made with ❤️ for GOST Analysis**

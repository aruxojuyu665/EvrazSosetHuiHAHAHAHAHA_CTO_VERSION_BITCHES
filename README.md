# ГОСТ Анализатор: RAG система для извлечения данных из стандартов

Проект для автоматического анализа и извлечения структурированных данных из документов стандартов ГОСТ с использованием RAG (Retrieval-Augmented Generation) подхода.

## Описание проекта

Система предназначена для автоматизации процесса сбора и структурирования технической информации из стандартов ГОСТ. Основная задача — извлечение данных о классах прочности стали, их химическом составе, механических свойствах и других характеристиках, а также выявление взаимосвязей между различными стандартами.

## Архитектура

Система построена на следующих компонентах:

- **LLM**: Claude 3.5 Sonnet через OpenRouter API
- **Embeddings**: OpenAI text-embedding-3-small
- **Vector Database**: Milvus
- **RAG Framework**: LlamaIndex
- **Deployment**: Docker + RunPod

## Структура проекта

```
.
├── data/                    # Данные проекта
│   ├── raw/                 # Исходные файлы ГОСТ (PDF)
│   └── processed/           # Обработанные данные (JSON, CSV)
├── docs/                    # Документация
├── src/                     # Исходный код
│   ├── config.py            # Конфигурация системы
│   ├── main.py              # Точка входа
│   ├── rag/                 # RAG система
│   │   └── rag_system.py    # Основная логика RAG
│   ├── vector_store/        # Работа с Milvus
│   │   └── milvus_store.py  # Менеджер Milvus
│   ├── parsers/             # Парсеры PDF
│   ├── extractors/          # Извлечение данных
│   └── models/              # Модели данных
├── tests/                   # Тесты
├── notebooks/               # Jupyter notebooks
├── config/                  # Конфигурационные файлы
├── Dockerfile               # Docker образ
├── docker-compose.yml       # Docker Compose для локальной разработки
└── runpod_start.sh          # Скрипт запуска на RunPod
```

## Установка

### Локальная установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/aruxojuyu665/EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES.git
cd EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте переменные окружения:
```bash
cp .env.example .env
# Отредактируйте .env и добавьте ваши API ключи
```

### Запуск с Docker Compose

1. Настройте `.env` файл с API ключами

2. Запустите все сервисы:
```bash
docker-compose up -d
```

3. Проверьте статус:
```bash
docker-compose ps
```

## Использование

### 1. Индексирование документов

Сначала необходимо проиндексировать документы ГОСТ:

```bash
python -m src.main index --input data/raw/GOST_27772-2021.pdf --create-new
```

Опции:
- `--input`: Путь к PDF файлу или директории с файлами
- `--create-new`: Создать новый индекс (удалит существующий)

### 2. Извлечение информации о классе прочности

Извлечение всей информации о конкретном классе прочности:

```bash
python -m src.main extract --class-name C235 --output data/processed/C235_info.json
```

Опции:
- `--class-name`: Название класса прочности (по умолчанию: C235)
- `--output`: Файл для сохранения результата

### 3. Произвольный запрос

Задайте любой вопрос по документу:

```bash
python -m src.main query --question "Какие требования к химическому составу стали класса C235?"
```

### 4. Статистика системы

Просмотр статистики индексированных документов:

```bash
python -m src.main stats
```

## Развертывание на RunPod

### Подготовка

1. Соберите Docker образ:
```bash
docker build -t gost-rag-system .
```

2. Загрузите образ в Docker Hub или используйте RunPod Template

### Запуск на RunPod

1. Создайте новый Pod на RunPod с следующими параметрами:
   - **Template**: Custom Docker Image
   - **Docker Image**: ваш образ
   - **Environment Variables**:
     - `OPENROUTER_API_KEY`: ваш ключ OpenRouter
     - `EMBEDDING_API_KEY`: ваш ключ для embeddings
     - `MILVUS_HOST`: адрес Milvus (если внешний)

2. Подключитесь к Pod через SSH или Web Terminal

3. Запустите систему:
```bash
bash /app/runpod_start.sh
```

## Конфигурация

Основные параметры настраиваются через переменные окружения в `.env`:

```env
# OpenRouter API
OPENROUTER_API_KEY=your_key
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet

# Embeddings
EMBEDDING_API_KEY=your_key
EMBEDDING_MODEL=text-embedding-3-small

# Milvus
MILVUS_HOST=localhost
MILVUS_PORT=19530

# RAG параметры
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
```

## Тестовая задача

Извлечь всю информацию о классе прочности стали **C235** из ГОСТ 27772-2021:

```bash
# 1. Индексирование
python -m src.main index --input data/raw/GOST_27772-2021.pdf --create-new

# 2. Извлечение информации
python -m src.main extract --class-name C235
```

Результат будет сохранен в `data/processed/C235_info.json` и будет включать:
- Химический состав
- Механические свойства
- Предельные отклонения
- Требования к испытаниям
- Ссылки на связанные стандарты

## Тестирование

Запуск тестов:

```bash
pytest tests/ -v
```

С покрытием кода:

```bash
pytest tests/ --cov=src --cov-report=html
```

## Технологии

- **Python**: 3.11
- **LLM**: Claude 3.5 Sonnet (через OpenRouter)
- **Embeddings**: OpenAI text-embedding-3-small
- **Vector DB**: Milvus 2.3.7
- **RAG Framework**: LlamaIndex 0.9.48
- **PDF Processing**: PyPDF2, pdfplumber
- **Deployment**: Docker, RunPod

## Документация

Полная документация проекта находится в директории `docs/`:
- [Техническое задание](docs/technical_specification.md)
- [Транскрипт встречи](docs/meeting_transcript.md)
- [Структура проекта](STRUCTURE.md)

## Разработка

### Создание новой ветки

```bash
git checkout -b feature/your-feature-name
```

### Код стайл

Проект следует PEP 8. Используйте:

```bash
# Форматирование
black src/

# Линтинг
pylint src/
```

## Лицензия

Проект разработан для внутреннего использования.

## Контакты

При возникновении вопросов обращайтесь к команде разработки.

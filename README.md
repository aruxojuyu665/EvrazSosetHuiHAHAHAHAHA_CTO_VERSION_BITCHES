# ГОСТ Анализатор: RAG система с веб-интерфейсом

[![Tests](https://img.shields.io/badge/tests-19%20passed-brightgreen)](TESTING_REPORT.md)
[![Coverage](https://img.shields.io/badge/coverage-100%25%20(tested%20modules)-brightgreen)](TESTING_REPORT.md)
[![Version](https://img.shields.io/badge/version-0.4.0-blue)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.11-blue)](requirements.txt)
[![Node.js](https://img.shields.io/badge/node.js-22-blue)](web/package.json)

Проект для автоматического анализа и извлечения структурированных данных из документов стандартов ГОСТ с использованием RAG (Retrieval-Augmented Generation) подхода. **Эта версия включает веб-интерфейс и использует Milvus Lite для упрощенного развертывания.**

---

## 📋 Описание проекта

Система предназначена для автоматизации процесса сбора и структурирования технической информации из стандартов ГОСТ. Основная задача — извлечение данных о классах прочности стали, их химическом составе, механических свойствах и других характеристиках, а также выявление взаимосвязей между различными стандартами.

### Ключевые возможности

✅ **Веб-интерфейс** - удобный UI для поиска и анализа
✅ **Индексирование PDF документов** - автоматическая обработка и векторизация
✅ **Семантический поиск** - поиск релевантной информации по запросу
✅ **Извлечение структурированных данных** - автоматическое извлечение характеристик классов прочности
✅ **Анализ взаимосвязей** - выявление ссылок между стандартами
✅ **Локальные эмбеддинги** - поддержка GPU, нулевая стоимость API, приватность
✅ **Milvus Lite** - упрощенное развертывание, не требует Docker

---

## 🏗️ Архитектура

Система состоит из двух основных частей: Python RAG API и Node.js веб-сервера.

| Компонент | Технология | Назначение |
|---|---|---|
| **Веб-интерфейс** | React 19, TypeScript, Tailwind CSS | Пользовательский интерфейс |
| **Веб-сервер** | Node.js, Express, tRPC | Backend для веб-интерфейса |
| **RAG API** | Python, FastAPI | API для RAG системы |
| **LLM** | Claude 3.5 Sonnet (OpenRouter) | Генерация ответов и анализ |
| **Embeddings** | Локальные (multilingual-e5-large) или OpenAI | Векторизация текста |
| **Vector Database** | Milvus Lite 2.3.5 | Хранение и поиск векторов (встроенная) |
| **RAG Framework** | LlamaIndex 0.10.68 | Оркестрация RAG pipeline |

**Подробнее:** [Архитектура системы](docs/SYSTEM_ARCHITECTURE.md)

---

## 🚀 Быстрый старт (с веб-интерфейсом)

### Требования
- Node.js 22+
- pnpm 9+
- Python 3.11+

### Установка

```bash
# 1. Клонировать репозиторий и перейти в нужную ветку
git clone https://github.com/aruxojuyu665/EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES.git
cd EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES
git checkout milvus-lite-migration

# 2. Установить зависимости Node.js
cd web
pnpm install
cd ..

# 3. Создать виртуальное окружение Python
python3.11 -m venv venv
source venv/bin/activate

# 4. Установить зависимости Python
pip install -r requirements.txt

# 5. Настроить переменные окружения
cp .env.example .env
# Отредактируйте .env и добавьте ваш OPENROUTER_API_KEY
```

### Запуск

**1. Запустить Python RAG API:**
```bash
source venv/bin/activate
python -m src.main api
# Запустится на http://localhost:8000
```

**2. Запустить Node.js backend + frontend:**
```bash
cd web
pnpm dev
# Запустится на http://localhost:3000
```

**Подробнее:** [QUICKSTART_LITE.md](docs/QUICKSTART_LITE.md)

---

## 📖 Использование

### Веб-интерфейс

После запуска откройте [http://localhost:3000](http://localhost:3000) в браузере.

### CLI команды

Система также предоставляет CLI для работы с RAG системой.

- `index` - Индексирование документов
- `extract` - Извлечение информации о классе прочности
- `query` - Произвольный запрос
- `stats` - Статистика системы
- `api` - Запуск FastAPI сервера

---

## ⚙️ Конфигурация

Основные параметры настраиваются через переменные окружения в `.env`.

```env
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Milvus Lite Configuration
APP_MILVUS_URI=./milvus_lite.db

# Web Server Configuration
RAG_API_URL=http://localhost:8000
```

---

## 🌐 Развертывание на RunPod

Развертывание на RunPod также упрощено. Docker больше не является обязательным для работы приложения.

**📘 [План развертывания с Milvus Lite](docs/RUNPOD_DEPLOYMENT_LITE.md)**

---

## 📚 Документация

- **[Быстрый старт (Milvus Lite)](docs/QUICKSTART_LITE.md)** - новое руководство по запуску
- **[Архитектура системы](docs/SYSTEM_ARCHITECTURE.md)** - логика работы и компоненты
- **[Структура проекта](STRUCTURE.md)** - описание структуры проекта


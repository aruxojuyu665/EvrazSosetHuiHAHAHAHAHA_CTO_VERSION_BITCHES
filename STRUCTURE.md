# Структура проекта GOST RAG

**Последнее обновление:** 01 ноября 2025 г.

Этот документ описывает структуру проекта, включая все директории и файлы, их назначение и функциональность.

## Корневая директория

| Файл/Директория | Описание |
|---|---|
| `src/` | Исходный код Python RAG системы |
| `web/` | Исходный код веб-интерфейса (Node.js + React) |
| `data/` | Данные проекта (PDF документы, и т.д.) |
| `docs/` | Документация проекта |
| `tests/` | Юнит-тесты |
| `config/` | Конфигурационные файлы (устарело) |
| `.env` | Переменные окружения (локальная конфигурация) |
| `.env.example` | Пример файла переменных окружения |
| `requirements.txt` | Зависимости Python |
| `package.json` | Зависимости Node.js (в `web/`) |
| `Dockerfile` | Dockerfile для CPU |
| `Dockerfile.gpu` | Dockerfile для GPU |
| `docker-compose.yml` | Docker Compose для CPU |
| `docker-compose.gpu.yml` | Docker Compose для GPU |
| `README.md` | Основная документация |
| `CHANGELOG.md` | История изменений |
| `STRUCTURE.md` | Этот файл |

## Python RAG система (`src/`)

| Файл/Директория | Описание |
|---|---|
| `main.py` | Главный файл для запуска CLI |
| `config.py` | Валидация и загрузка конфигурации из `.env` |
| `rag/rag_system.py` | Основной класс RAG системы (LlamaIndex) |
| `vector_store/milvus_store.py` | Менеджер для работы с Milvus Lite |
| `parsers/pdf_parser.py` | Парсер для PDF документов |
| `extractors/data_extractor.py` | Извлечение структурированных данных |
| `models/strength_class.py` | Pydantic модель для класса прочности |
| `utils/retry_decorator.py` | Декоратор для повторных попыток |

## Веб-интерфейс (`web/`)

### Frontend (`web/client/`)

| Файл/Директория | Описание |
|---|---|
| `src/App.tsx` | Главный компонент приложения, роутинг |
| `src/pages/Home.tsx` | Главная страница с поиском |
| `src/pages/ComponentShowcase.tsx` | Страница с демонстрацией UI компонентов |
| `src/components/` | UI компоненты (shadcn/ui) |
| `src/contexts/` | React контексты (тема, и т.д.) |
| `src/hooks/` | React хуки |
| `src/main.tsx` | Точка входа в приложение |

### Backend (`web/server/`)

| Файл/Директория | Описание |
|---|---|
| `index.ts` | Главный файл Node.js сервера (Express) |
| `routers.ts` | Главный tRPC роутер |
| `ragRouter.ts` | tRPC роутер для RAG API |
| `ragClient.ts` | HTTP клиент для связи с Python RAG API |
| `db.ts` | Настройка Drizzle ORM и подключения к БД |
| `storage.ts`| Работа с файловым хранилищем |
| `_core/` | Инфраструктурный код (tRPC, env, и т.д.) |

### Общий код (`web/shared/`)

| Файл/Директория | Описание |
|---|---|
| `types.ts` | Общие TypeScript типы |
| `const.ts` | Общие константы |

## Документация (`docs/`)

| Файл/Директория | Описание |
|---|---|
| `AnotherDocs/` | Архив старой документации |
| `QUICKSTART_LITE.md` | Инструкция по быстрому старту |
| `RUNPOD_DEPLOYMENT_LITE.md` | Инструкция по развертыванию на RunPod |
| `MILVUS_LITE_MIGRATION.md` | План миграции на Milvus Lite |
| `SYSTEM_ARCHITECTURE.md` | Описание архитектуры системы |
| `tech_stack.md` | Технологический стек проекта |

---


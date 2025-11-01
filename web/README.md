# GOST RAG Web Interface

Web-интерфейс для системы анализа документов ГОСТ с использованием RAG (Retrieval-Augmented Generation).

## Технологии

### Frontend
- **React 19** - UI библиотека
- **TypeScript** - типизация
- **Tailwind CSS 4** - стилизация
- **shadcn/ui** - компоненты UI
- **Vite** - сборщик
- **Wouter** - роутинг

### Backend
- **Node.js** - runtime
- **Express 4** - веб-сервер
- **tRPC 11** - type-safe API
- **Drizzle ORM** - работа с БД
- **MySQL/TiDB** - база данных

### Интеграция
- **FastAPI** - Python RAG backend
- **HTTP Client** - связь Node.js ↔ Python

## Структура проекта

```
web/
├── client/              # Frontend (React)
│   ├── src/
│   │   ├── pages/      # Страницы приложения
│   │   ├── components/ # UI компоненты
│   │   ├── lib/        # Утилиты
│   │   └── App.tsx     # Главный компонент
│   └── public/         # Статические файлы
├── server/             # Backend (Node.js + tRPC)
│   ├── routers.ts      # API endpoints
│   ├── ragRouter.ts    # RAG API endpoints
│   ├── ragClient.ts    # Python RAG client
│   └── _core/          # Инфраструктура
├── shared/             # Общий код
│   ├── types.ts        # TypeScript типы
│   └── const.ts        # Константы
└── python_rag/         # Python RAG система
    ├── api_server.py   # FastAPI сервер
    ├── src/            # RAG код
    └── config.yaml     # Конфигурация
```

## Установка

### Требования
- Node.js 22+
- pnpm 9+
- Python 3.11+ (для RAG backend)

### Установка зависимостей

```bash
# Frontend + Backend
pnpm install

# Python RAG backend
cd python_rag
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или: venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Запуск

### Development

**1. Запустить Python RAG API:**
```bash
cd python_rag
source venv/bin/activate
python api_server.py
# Запустится на http://localhost:8000
```

**2. Запустить Node.js backend + frontend:**
```bash
pnpm dev
# Запустится на http://localhost:3000
```

### Production

```bash
# Build
pnpm build

# Start
pnpm start
```

## Переменные окружения

Создайте `.env` файл:

```bash
# Database
DATABASE_URL=mysql://user:password@host:port/database

# OpenRouter API (для LLM)
OPENROUTER_API_KEY=sk-or-v1-...

# RAG API URL
RAG_API_URL=http://localhost:8000

# JWT Secret
JWT_SECRET=your-secret-key

# OAuth (опционально)
OAUTH_SERVER_URL=...
VITE_OAUTH_PORTAL_URL=...
```

## Функциональность

### Реализовано ✅

**Frontend:**
- Главная страница с интерфейсом поиска
- Форма семантического поиска по документам
- Форма извлечения информации о классе прочности
- Dashboard с системной статистикой
- Отображение результатов в Markdown
- Responsive дизайн

**Backend:**
- tRPC API endpoints:
  - `rag.query` - семантический поиск
  - `rag.extract` - извлечение информации о классе
  - `rag.getStats` - системная статистика
  - `rag.healthCheck` - проверка здоровья RAG API
- HTTP клиент для Python RAG API
- Error handling и fallback

**Python RAG API:**
- FastAPI сервер на порту 8000
- Endpoints: `/health`, `/stats`, `/query`, `/extract`
- Интеграция с LlamaIndex
- Поддержка Milvus Lite (после миграции)

### В разработке 🚧

- Загрузка документов через UI
- История запросов
- Экспорт результатов (PDF, Markdown)
- Настройки системы
- Мониторинг производительности

## API Endpoints

### tRPC (Node.js)

```typescript
// Поиск по документам
const result = await trpc.rag.query.mutate({
  question: "Какие характеристики у класса C235?"
});

// Извлечение информации о классе
const result = await trpc.rag.extract.mutate({
  className: "C235"
});

// Статистика системы
const stats = await trpc.rag.getStats.query();

// Проверка здоровья
const health = await trpc.rag.healthCheck.query();
```

### Python RAG API

```bash
# Health check
curl http://localhost:8000/health

# Stats
curl http://localhost:8000/stats

# Query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Характеристики C235?"}'

# Extract
curl -X POST http://localhost:8000/extract \
  -H "Content-Type: application/json" \
  -d '{"class_name": "C235"}'
```

## Разработка

### Добавление новых endpoints

1. Добавить endpoint в `server/ragRouter.ts`
2. Использовать `ragClient` для вызова Python API
3. Добавить типы в `shared/types.ts`
4. Использовать в компонентах через `trpc.rag.*`

### Добавление новых страниц

1. Создать компонент в `client/src/pages/`
2. Добавить роут в `client/src/App.tsx`
3. Добавить навигацию (если нужно)

### Стилизация

- Используйте Tailwind CSS классы
- Используйте shadcn/ui компоненты из `@/components/ui/`
- Следуйте существующему дизайну

## Тестирование

```bash
# Unit тесты
pnpm test

# Type checking
pnpm typecheck

# Linting
pnpm lint
```

## Deployment

### Требования
- Node.js 22+
- MySQL/TiDB database
- Python 3.11+ с GPU (для embeddings)

### Шаги

1. Build приложения:
```bash
pnpm build
```

2. Настроить переменные окружения

3. Запустить Python RAG API:
```bash
cd python_rag
source venv/bin/activate
python api_server.py
```

4. Запустить Node.js сервер:
```bash
pnpm start
```

5. Настроить reverse proxy (nginx/caddy)

## Архитектура

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────────────┐
│  Node.js + tRPC     │
│  (Port 3000)        │
└──────┬──────────────┘
       │ HTTP
       ▼
┌─────────────────────┐
│  Python FastAPI     │
│  (Port 8000)        │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  RAG System         │
│  - LlamaIndex       │
│  - Milvus Lite      │
│  - GPU Embeddings   │
│  - Claude 3.5       │
└─────────────────────┘
```

## Известные проблемы

1. **TypeScript error в main.tsx** - не критично, не влияет на работу
2. **RAG API требует миграции на Milvus Lite** - в процессе (см. docs/MILVUS_LITE_MIGRATION.md)

## Лицензия

Проприетарный проект для анализа документов ГОСТ.

## Контакты

- GitHub: https://github.com/aruxojuyu665/EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES
- Ветка: milvus-lite-migration

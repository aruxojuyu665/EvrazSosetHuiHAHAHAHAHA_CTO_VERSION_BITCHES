# Code Review: Веб-интерфейс (v0.4.0)

**Дата:** 2025-11-01  
**Ревьюер:** Manus AI  
**Версия:** 0.4.0  
**Ветка:** milvus-lite-migration

## Общая информация

Проведен анализ кодовой базы веб-интерфейса для RAG системы ГОСТ Анализатор. Веб-интерфейс состоит из:
- **Frontend:** React 19 + TypeScript + Tailwind CSS + shadcn/ui
- **Backend:** Node.js + Express + tRPC
- **Интеграция:** HTTP клиент для связи с Python FastAPI

## Найденные проблемы

### P1 (Critical) - 2 проблемы

#### P1-1: Отсутствует обработка ошибок сети в ragClient
**Файл:** `web/server/ragClient.ts`  
**Проблема:** Методы `query()` и `extract()` не обрабатывают сетевые ошибки (timeout, connection refused).

**Текущий код:**
```typescript
async query(question: string): Promise<QueryResponse> {
  const response = await fetch(`${this.baseUrl}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
  if (!response.ok) {
    throw new Error(`Query failed: ${response.statusText}`);
  }
  return response.json();
}
```

**Рекомендация:** Добавить try-catch и обработку timeout.

---

#### P1-2: Отсутствует валидация ответа API
**Файл:** `web/server/ragClient.ts`  
**Проблема:** Не проверяется структура ответа от API перед использованием.

**Рекомендация:** Добавить валидацию с помощью Zod или аналога.

---

### P2 (Important) - 3 проблемы

#### P2-1: Hardcoded API URL в ragClient
**Файл:** `web/server/ragClient.ts:6`  
**Проблема:** URL API захардкожен как `http://localhost:8000`, что не работает в production.

**Текущий код:**
```typescript
const RAG_API_URL = process.env.RAG_API_URL || "http://localhost:8000";
```

**Рекомендация:** Использовать переменную окружения без fallback или добавить проверку.

---

#### P2-2: Отсутствует retry логика для API запросов
**Файл:** `web/server/ragClient.ts`  
**Проблема:** При временных сбоях API запросы не повторяются.

**Рекомендация:** Добавить retry логику с экспоненциальной задержкой.

---

#### P2-3: Отсутствует кэширование статистики
**Файл:** `web/client/src/pages/Home.tsx:20`  
**Проблема:** Статистика запрашивается каждые 10 секунд без кэширования.

**Текущий код:**
```typescript
const { data: stats, isLoading: statsLoading } = trpc.rag.getStats.useQuery(undefined, {
  refetchInterval: 10000, // Refresh every 10 seconds
});
```

**Рекомендация:** Использовать stale-while-revalidate стратегию.

---

### P3 (Minor) - 2 проблемы

#### P3-1: Отсутствует loading state для результатов
**Файл:** `web/client/src/pages/Home.tsx:190`  
**Проблема:** При загрузке результатов не показывается skeleton или spinner.

**Рекомендация:** Добавить loading state.

---

#### P3-2: Неполная типизация в Home.tsx
**Файл:** `web/client/src/pages/Home.tsx:30,41`  
**Проблема:** Используется `any` для типа error.

**Текущий код:**
```typescript
onError: (error: any) => {
  toast.error(`Ошибка: ${error.message}`);
},
```

**Рекомендация:** Использовать правильный тип из tRPC.

---

## Положительные моменты

✅ **Хорошая архитектура:** Четкое разделение frontend/backend  
✅ **Современный стек:** React 19, TypeScript, tRPC  
✅ **UI компоненты:** Использование shadcn/ui для консистентного дизайна  
✅ **Типизация:** Большая часть кода типизирована  
✅ **UX:** Хорошие toast уведомления и feedback

## Итоговая оценка

**Общая оценка:** 8/10 ⭐

**Распределение проблем:**
- P1 (Critical): 2
- P2 (Important): 3
- P3 (Minor): 2

**Рекомендации:**
1. Исправить P1-1 и P1-2 перед production
2. Добавить retry логику (P2-2)
3. Улучшить обработку ошибок

## Следующие шаги

1. Исправить критические проблемы (P1)
2. Исправить важные проблемы (P2)
3. Провести локальное тестирование
4. Задокументировать API интеграцию

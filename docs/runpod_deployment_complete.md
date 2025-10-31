# GOST RAG System - Развертывание на RunPod ЗАВЕРШЕНО ✅

**Дата:** 30 октября 2025  
**Сервер:** RunPod GPU Instance (RTX 3090, 24GB VRAM)  
**Статус:** Готово к использованию

---

## Информация о сервере

**Подключение:**
```bash
ssh root@213.192.2.89 -p 40039 -i ~/.ssh/id_ed25519
```

**Характеристики:**
- **GPU:** NVIDIA GeForce RTX 3090 (24 GB VRAM)
- **CPU:** 32 vCPU
- **RAM:** 125 GB
- **Storage:** 199 TB доступно в /workspace
- **OS:** Ubuntu 24.04 (Noble)
- **Python:** 3.11.14

---

## Установленное ПО

### Python окружение
- **Путь:** `/workspace/gost_rag/venv/`
- **Python:** 3.11.14
- **pip:** 25.3

### Ключевые пакеты
| Пакет | Версия | Назначение |
|-------|--------|------------|
| torch | 2.9.0 | Deep Learning (с CUDA 12.8) |
| llama-index | 0.14.6 | RAG Framework |
| llama-index-core | 0.14.6 | Core RAG функции |
| llama-index-llms-openai | 0.6.6 | OpenRouter интеграция |
| llama-index-embeddings-huggingface | 0.6.1 | Локальные эмбеддинги |
| llama-index-vector-stores-milvus | 0.9.3 | Milvus интеграция |
| transformers | 4.57.1 | HuggingFace Transformers |
| sentence-transformers | 5.1.2 | Sentence embeddings |
| pymilvus | 2.6.2 | Milvus Python SDK |
| milvus | 2.3.5 | Milvus Lite (embedded) |
| pandas | 2.2.3 | Data processing |
| numpy | 2.3.4 | Numerical computing |

### CUDA библиотеки
- nvidia-cublas-cu12: 12.8.4.1
- nvidia-cudnn-cu12: 9.6.0.74
- nvidia-cusparse-cu12: 12.8.4.1
- nvidia-cusolver-cu12: 11.8.4.1
- nvidia-cufft-cu12: 11.4.4.1
- nvidia-curand-cu12: 10.4.4.1
- nvidia-nccl-cu12: 2.25.3

---

## Структура проекта

```
/workspace/gost_rag/
├── venv/                    # Python виртуальное окружение
├── src/                     # Исходный код
│   ├── config.py           # Конфигурация
│   ├── main.py             # Точка входа
│   ├── parsers/            # PDF парсеры
│   ├── extractors/         # Извлечение данных
│   ├── models/             # Модели данных
│   ├── rag/                # RAG система
│   ├── vector_store/       # Milvus менеджер
│   └── utils/              # Утилиты
├── data/
│   ├── raw/                # Исходные PDF (ГОСТ 27772-2021)
│   └── processed/          # Обработанные данные
├── tests/                  # Тесты
├── docs/                   # Документация
├── config.yaml             # Конфигурация системы
├── requirements.txt        # Python зависимости
└── README.md              # Основная документация
```

---

## Конфигурация

Файл: `/workspace/gost_rag/config.yaml`

```yaml
embedding:
  type: local
  model: intfloat/multilingual-e5-large
  device: cuda

milvus:
  host: localhost
  port: 19530
  collection_name: gost_documents

llm:
  provider: openrouter
  model: anthropic/claude-3.5-sonnet
  api_key: ${OPENROUTER_API_KEY}
  temperature: 0.1
  max_tokens: 4096

chunking:
  chunk_size: 1000
  chunk_overlap: 200

paths:
  data_dir: /workspace/gost_rag/data
  raw_dir: /workspace/gost_rag/data/raw
  processed_dir: /workspace/gost_rag/data/processed
```

---

## Запуск системы

### 1. Подключиться к серверу
```bash
ssh root@213.192.2.89 -p 40039 -i ~/.ssh/id_ed25519
```

### 2. Активировать виртуальное окружение
```bash
cd /workspace/gost_rag
source venv/bin/activate
```

### 3. Установить переменные окружения
```bash
export OPENROUTER_API_KEY="your_api_key_here"
export EMBEDDING_TYPE="local"
export EMBEDDING_DEVICE="cuda"
```

### 4. Индексировать документы
```bash
python -m src.main index --input data/raw --create-new
```

### 5. Извлечь информацию о классе прочности
```bash
python -m src.main extract --class-name C235
```

### 6. Выполнить произвольный запрос
```bash
python -m src.main query --question "Какие требования к химическому составу стали класса C235?"
```

### 7. Получить статистику
```bash
python -m src.main stats
```

---

## Проверка GPU

```bash
# Проверить доступность CUDA
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"

# Ожидаемый вывод:
# CUDA available: True
# GPU: NVIDIA GeForce RTX 3090
```

---

## Мониторинг

### Использование GPU
```bash
nvidia-smi
```

### Использование диска
```bash
df -h /workspace
```

### Использование памяти
```bash
free -h
```

### Процессы Python
```bash
ps aux | grep python
```

---

## Следующие шаги

### 1. Настроить API ключи
- Получить OpenRouter API ключ: https://openrouter.ai/
- Установить в переменную окружения `OPENROUTER_API_KEY`

### 2. Загрузить дополнительные документы ГОСТ
```bash
# Скопировать PDF файлы в data/raw/
scp -P 40039 -i ~/.ssh/id_ed25519 *.pdf root@213.192.2.89:/workspace/gost_rag/data/raw/
```

### 3. Запустить веб-интерфейс
```bash
# TODO: Интегрировать веб-интерфейс из gost_rag_web проекта
```

### 4. Настроить автозапуск (systemd)
```bash
# TODO: Создать systemd service для автоматического запуска
```

---

## Troubleshooting

### Проблема: Out of Memory (OOM)
**Решение:**
```bash
# Уменьшить batch size в config.yaml
# Или использовать CPU для эмбеддингов:
export EMBEDDING_DEVICE="cpu"
```

### Проблема: CUDA not available
**Решение:**
```bash
# Проверить драйверы NVIDIA
nvidia-smi

# Переустановить PyTorch с CUDA
pip install torch==2.9.0 --index-url https://download.pytorch.org/whl/cu121
```

### Проблема: Milvus connection error
**Решение:**
```bash
# Milvus Lite работает embedded, не требует отдельного сервера
# Проверить что milvus установлен:
pip list | grep milvus
```

---

## Производительность

### Ожидаемая скорость

| Операция | Время (GPU) | Время (CPU) |
|----------|-------------|-------------|
| Индексация 1 PDF (50 стр) | ~30 сек | ~2 мин |
| Генерация эмбеддинга (1 chunk) | ~0.01 сек | ~0.1 сек |
| Поиск в векторной БД | ~0.05 сек | ~0.05 сек |
| Генерация ответа (LLM) | ~2-5 сек | ~2-5 сек |

### Оптимизация
- **GPU:** RTX 3090 идеально подходит для локальных эмбеддингов
- **Batch processing:** Обрабатывать документы пакетами по 10-20
- **Кэширование:** Эмбеддинги кэшируются в Milvus

---

## Стоимость

### RunPod Instance
- **Compute:** $0.46/час (~$331/месяц)
- **Storage (100 GB):** $0.0133/час (~$10/месяц)
- **Итого:** ~$341/месяц

### API (OpenRouter)
- **Claude 3.5 Sonnet:** $3/$15 за 1M tokens (input/output)
- **Ожидаемое использование:** ~$50-100/месяц

**Общая стоимость:** ~$391-441/месяц

---

## Контакты и поддержка

**Репозиторий:** https://github.com/aruxojuyu665/EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES  
**Ветка:** RAG-Milvus-Manus-Edition  
**Документация:** /workspace/gost_rag/docs/

---

## Статус развертывания

- ✅ Python 3.11 установлен
- ✅ Виртуальное окружение создано
- ✅ Все зависимости установлены
- ✅ PyTorch с CUDA настроен
- ✅ Milvus Lite установлен
- ✅ Конфигурация создана
- ✅ Код загружен
- ⏳ API ключи (требуется настройка)
- ⏳ Индексация документов (требуется запуск)
- ⏳ Веб-интерфейс (требуется интеграция)

**Система готова к использованию после настройки API ключей!** 🚀

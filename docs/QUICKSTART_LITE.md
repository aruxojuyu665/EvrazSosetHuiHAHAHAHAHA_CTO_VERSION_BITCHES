# Быстрый старт с Milvus Lite

Эта инструкция описывает, как быстро запустить проект после миграции на Milvus Lite. Основное преимущество — **отсутствие необходимости в Docker** для векторной базы данных.

---

## Требования

- **Python 3.11**
- **Git**
- **API ключ OpenRouter**
- **GPU с поддержкой CUDA** (опционально, для ускорения локальных эмбеддингов)

---

## Пошаговая инструкция

### 1. Клонирование репозитория

Клонируйте репозиторий и перейдите в ветку `milvus-lite-migration`:

```bash
git clone https://github.com/aruxojuyu665/EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES.git
cd EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES
git checkout milvus-lite-migration
```

### 2. Создание виртуального окружения

Изолируйте зависимости проекта с помощью виртуального окружения:

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

Установите все необходимые пакеты, включая `milvus-lite`:

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Скопируйте пример файла `.env` и добавьте ваш API ключ:

```bash
cp .env.example .env
```

Откройте файл `.env` в текстовом редакторе и вставьте ваш ключ в `OPENROUTER_API_KEY`:

```env
# .env
OPENROUTER_API_KEY=your_openrouter_api_key_here
...
```

### 5. Индексирование документов

Запустите процесс индексирования. Milvus Lite автоматически создаст файл базы данных `milvus_lite.db` в корне проекта.

```bash
python -m src.main index --input data/raw/GOST_27772-2021.pdf --create-new
```

- `--input`: Указывает на файл или директорию с документами для индексации.
- `--create-new`: Удаляет существующую коллекцию и создает новую.

### 6. Выполнение запросов

Теперь вы можете выполнять запросы к системе.

#### Извлечение информации о классе прочности:

```bash
python -m src.main extract --class-name C235
```

#### Произвольный вопрос:

```bash
python -m src.main query --question "Какой химический состав у стали C345?"
```

### 7. Просмотр статистики

Чтобы проверить состояние коллекции Milvus Lite, используйте команду `stats`:

```bash
python -m src.main stats
```

---

## Что дальше?

- **[План развертывания на RunPod](RUNPOD_DEPLOYMENT_LITE.md)**: Инструкции по деплою на сервер.
- **[Отчет Code Review](CODE_REVIEW_MILVUS_LITE.md)**: Подробный анализ изменений и исправлений.

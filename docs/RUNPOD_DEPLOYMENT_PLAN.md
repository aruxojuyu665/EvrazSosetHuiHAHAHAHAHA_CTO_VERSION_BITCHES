# План развертывания RAG системы на RunPod

**Дата:** 30 октября 2025  
**Версия:** 0.2.1  
**Цель:** Пошаговое развертывание RAG системы на выделенном сервере RunPod

---

## Содержание

1. [Требования к серверу](#требования-к-серверу)
2. [Предварительная подготовка](#предварительная-подготовка)
3. [Пошаговая инструкция](#пошаговая-инструкция)
4. [Проверка работоспособности](#проверка-работоспособности)
5. [Мониторинг и обслуживание](#мониторинг-и-обслуживание)
6. [Troubleshooting](#troubleshooting)

---

## Требования к серверу

### Минимальные требования

| Компонент | Минимум | Рекомендуется |
|-----------|---------|---------------|
| **CPU** | 4 vCPU @ 2.5 GHz | 8 vCPU @ 3.0 GHz+ |
| **RAM** | 16 GB | 32 GB |
| **Storage** | 100 GB SSD | 200 GB SSD |
| **Network** | 100 Mbps | 1 Gbps |
| **GPU** | Не требуется | Не требуется |
| **OS** | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |

### Рекомендуемая конфигурация RunPod

**Pod Type:** CPU Pod  
**Template:** Ubuntu 22.04 LTS  
**vCPU:** 8 cores  
**RAM:** 32 GB  
**Storage:** 200 GB SSD  
**Network:** 1 Gbps  

**Стоимость:** ~$0.20-0.30/час (~$144-216/месяц)

---

## Предварительная подготовка

### 1. Получение API ключей

Перед развертыванием необходимо получить следующие API ключи:

#### OpenRouter API Key
1. Зарегистрироваться на https://openrouter.ai
2. Перейти в раздел API Keys
3. Создать новый ключ
4. Сохранить ключ в безопасном месте

**Модель:** `anthropic/claude-3.5-sonnet`  
**Стоимость:** ~$3 за 1M input tokens, ~$15 за 1M output tokens

#### OpenAI API Key (для embeddings)
1. Зарегистрироваться на https://platform.openai.com
2. Перейти в раздел API Keys
3. Создать новый ключ
4. Сохранить ключ в безопасном месте

**Модель:** `text-embedding-3-small`  
**Стоимость:** ~$0.02 за 1M tokens

### 2. Подготовка документов

Подготовить документы ГОСТ в формате PDF для индексирования:
- GOST_27772-2021.pdf (уже есть в репозитории)
- Дополнительные документы (опционально)

### 3. Создание RunPod Pod

1. Войти в RunPod: https://www.runpod.io
2. Перейти в раздел "Pods"
3. Нажать "Deploy"
4. Выбрать "CPU Pods"
5. Выбрать конфигурацию:
   - **Template:** Ubuntu 22.04 LTS
   - **vCPU:** 8 cores
   - **RAM:** 32 GB
   - **Storage:** 200 GB SSD
6. Включить SSH доступ
7. Нажать "Deploy"
8. Дождаться запуска Pod
9. Сохранить SSH credentials

---

## Пошаговая инструкция

### Шаг 1: Подключение к серверу

```bash
# Получить SSH команду из RunPod dashboard
ssh root@<pod-ip> -p <port> -i ~/.ssh/id_rsa

# Или использовать пароль
ssh root@<pod-ip> -p <port>
```

**Проверка подключения:**
```bash
# Проверить версию ОС
cat /etc/os-release

# Проверить ресурсы
free -h
df -h
nproc
```

---

### Шаг 2: Обновление системы

```bash
# Обновить список пакетов
apt update

# Обновить установленные пакеты
apt upgrade -y

# Установить базовые утилиты
apt install -y \
    curl \
    wget \
    git \
    vim \
    htop \
    net-tools \
    build-essential
```

**Время выполнения:** 5-10 минут

---

### Шаг 3: Установка Docker и Docker Compose

```bash
# Установить Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Запустить Docker
systemctl start docker
systemctl enable docker

# Проверить установку
docker --version

# Установить Docker Compose
apt install -y docker-compose

# Проверить установку
docker-compose --version
```

**Ожидаемый вывод:**
```
Docker version 24.0.x
docker-compose version 1.29.x
```

**Время выполнения:** 3-5 минут

---

### Шаг 4: Клонирование репозитория

```bash
# Перейти в домашнюю директорию
cd /root

# Клонировать репозиторий
git clone https://github.com/aruxojuyu665/EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES.git

# Перейти в директорию проекта
cd EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES

# Переключиться на рабочую ветку
git checkout RAG-Milvus-Manus-Edition

# Проверить структуру
ls -la
```

**Ожидаемая структура:**
```
.
├── data/
├── docs/
├── src/
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
└── ...
```

**Время выполнения:** 1-2 минуты

---

### Шаг 5: Настройка переменных окружения

```bash
# Скопировать пример конфигурации
cp .env.example .env

# Отредактировать .env файл
vim .env
```

**Необходимо заполнить:**
```bash
# OpenRouter API Configuration
OPENROUTER_API_KEY=<ваш_openrouter_api_key>
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet

# Embedding Model Configuration
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_API_KEY=<ваш_openai_api_key>

# Milvus Configuration
MILVUS_HOST=milvus-standalone
MILVUS_PORT=19530
MILVUS_COLLECTION_NAME=gost_documents

# MinIO Configuration (ВАЖНО: изменить для production!)
MINIO_ACCESS_KEY=<сгенерировать_сложный_ключ>
MINIO_SECRET_KEY=<сгенерировать_сложный_секрет>

# Application Settings
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
TEMPERATURE=0.1
MAX_TOKENS=4096
```

**Генерация безопасных ключей для MinIO:**
```bash
# Сгенерировать случайные ключи
openssl rand -base64 32  # Для MINIO_ACCESS_KEY
openssl rand -base64 32  # Для MINIO_SECRET_KEY
```

**Время выполнения:** 2-3 минуты

---

### Шаг 6: Запуск системы через Docker Compose

```bash
# Убедиться что находимся в директории проекта
cd /root/EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES

# Запустить все сервисы
docker-compose up -d

# Проверить статус контейнеров
docker-compose ps
```

**Ожидаемый вывод:**
```
NAME                    STATUS          PORTS
milvus-etcd            Up 30 seconds   2379-2380/tcp
milvus-minio           Up 30 seconds   9000-9001/tcp
milvus-standalone      Up 20 seconds   19530/tcp, 9091/tcp
rag-app                Up 10 seconds   
```

**Проверка логов:**
```bash
# Логи Milvus
docker-compose logs milvus-standalone

# Логи приложения
docker-compose logs rag-app

# Следить за логами в реальном времени
docker-compose logs -f
```

**Время выполнения:** 5-10 минут (скачивание образов)

---

### Шаг 7: Проверка работоспособности Milvus

```bash
# Подключиться к контейнеру приложения
docker-compose exec rag-app bash

# Проверить подключение к Milvus (внутри контейнера)
python3 -c "from pymilvus import connections; connections.connect(host='milvus-standalone', port='19530'); print('Milvus connected successfully!')"
```

**Ожидаемый вывод:**
```
Milvus connected successfully!
```

**Если ошибка:**
```bash
# Проверить что Milvus запущен
docker-compose ps milvus-standalone

# Перезапустить Milvus
docker-compose restart milvus-standalone

# Подождать 30 секунд и повторить проверку
```

**Время выполнения:** 1-2 минуты

---

### Шаг 8: Индексирование документов

```bash
# Внутри контейнера rag-app
cd /app

# Индексировать тестовый документ
python -m src.main index \
    --input /app/data/raw/GOST_27772-2021.pdf \
    --create-new

# Проверить статистику
python -m src.main stats
```

**Ожидаемый вывод:**
```
Индексирование документов из: /app/data/raw/GOST_27772-2021.pdf
Загружено документов: 1
Создание индекса...
[████████████████████████████████████████] 100%
Индексирование завершено

Статистика коллекции:
- Название: gost_documents
- Количество векторов: 245
- Размерность: 1536
```

**Время выполнения:** 2-5 минут (зависит от размера документа)

---

### Шаг 9: Тестирование запросов

```bash
# Простой запрос
python -m src.main query \
    --question "Что такое класс прочности C235?" \
    --output /app/output/test_query.json

# Извлечение информации о классе прочности
python -m src.main extract \
    --class-name C235 \
    --output /app/output/c235_info.json

# Проверить результаты
cat /app/output/test_query.json
cat /app/output/c235_info.json
```

**Ожидаемый вывод:**
```json
{
  "answer": "Класс прочности C235 - это...",
  "source_nodes": [...],
  "metadata": {...}
}
```

**Время выполнения:** 5-10 секунд на запрос

---

### Шаг 10: Настройка автозапуска

```bash
# Выйти из контейнера
exit

# Создать systemd service для автозапуска
cat > /etc/systemd/system/rag-system.service << 'EOF'
[Unit]
Description=RAG System for GOST Analysis
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/root/EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

# Включить автозапуск
systemctl enable rag-system.service

# Проверить статус
systemctl status rag-system.service
```

**Время выполнения:** 1-2 минуты

---

## Проверка работоспособности

### Чек-лист проверки

- [ ] Docker установлен и запущен
- [ ] Docker Compose установлен
- [ ] Репозиторий склонирован
- [ ] Переменные окружения настроены
- [ ] Все контейнеры запущены (4/4)
- [ ] Milvus доступен
- [ ] Документы проиндексированы
- [ ] Запросы работают
- [ ] Автозапуск настроен

### Команды для проверки

```bash
# Проверка Docker
docker --version
docker ps

# Проверка контейнеров
docker-compose ps

# Проверка Milvus
docker-compose exec rag-app python3 -c "from pymilvus import connections; connections.connect(host='milvus-standalone', port='19530'); print('OK')"

# Проверка индекса
docker-compose exec rag-app python -m src.main stats

# Тестовый запрос
docker-compose exec rag-app python -m src.main query --question "Тест"
```

### Метрики производительности

**Ожидаемые значения:**

| Метрика | Значение |
|---------|----------|
| Время индексирования (10 страниц) | < 2 минуты |
| Время запроса (простой) | 2-5 секунд |
| Время запроса (сложный) | 5-10 секунд |
| Использование RAM | 8-12 GB |
| Использование CPU | 20-40% |
| Использование Disk | 10-20 GB |

---

## Мониторинг и обслуживание

### Мониторинг ресурсов

```bash
# Использование ресурсов контейнерами
docker stats

# Использование диска
df -h

# Использование памяти
free -h

# Нагрузка на CPU
htop
```

### Логи

```bash
# Все логи
docker-compose logs

# Логи конкретного сервиса
docker-compose logs milvus-standalone
docker-compose logs rag-app

# Следить за логами
docker-compose logs -f --tail=100
```

### Резервное копирование

```bash
# Создать backup Milvus данных
docker-compose exec milvus-standalone \
    tar -czf /tmp/milvus-backup.tar.gz /var/lib/milvus

# Скопировать backup на хост
docker cp milvus-standalone:/tmp/milvus-backup.tar.gz \
    /root/backups/milvus-backup-$(date +%Y%m%d).tar.gz

# Backup MinIO данных
docker-compose exec minio \
    tar -czf /tmp/minio-backup.tar.gz /minio_data

docker cp milvus-minio:/tmp/minio-backup.tar.gz \
    /root/backups/minio-backup-$(date +%Y%m%d).tar.gz
```

### Обновление системы

```bash
# Перейти в директорию проекта
cd /root/EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES

# Получить обновления
git pull origin RAG-Milvus-Manus-Edition

# Пересобрать образы
docker-compose build

# Перезапустить сервисы
docker-compose down
docker-compose up -d
```

---

## Troubleshooting

### Проблема 1: Milvus не запускается

**Симптомы:**
```
milvus-standalone    Exit 1
```

**Решение:**
```bash
# Проверить логи
docker-compose logs milvus-standalone

# Проверить порты
netstat -tulpn | grep 19530

# Очистить данные и перезапустить
docker-compose down -v
docker-compose up -d
```

---

### Проблема 2: Ошибка подключения к API

**Симптомы:**
```
Error: API key not configured
```

**Решение:**
```bash
# Проверить .env файл
cat .env | grep API_KEY

# Убедиться что ключи установлены
docker-compose exec rag-app env | grep API_KEY

# Перезапустить с новыми переменными
docker-compose down
docker-compose up -d
```

---

### Проблема 3: Недостаточно памяти

**Симптомы:**
```
OOMKilled
```

**Решение:**
```bash
# Проверить использование памяти
free -h
docker stats

# Увеличить swap
fallocate -l 8G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

# Добавить в /etc/fstab для постоянного использования
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

---

### Проблема 4: Медленные запросы

**Симптомы:**
- Запросы выполняются > 30 секунд

**Решение:**
```bash
# Проверить нагрузку
htop

# Проверить сеть
ping openrouter.ai
ping api.openai.com

# Увеличить timeout в .env
TIMEOUT=120

# Перезапустить
docker-compose restart rag-app
```

---

### Проблема 5: Контейнер постоянно перезапускается

**Симптомы:**
```
rag-app    Restarting (1) 10 seconds ago
```

**Решение:**
```bash
# Проверить логи
docker-compose logs rag-app

# Проверить зависимости
docker-compose exec rag-app pip list

# Переустановить зависимости
docker-compose build --no-cache rag-app
docker-compose up -d
```

---

## Контакты и поддержка

**Репозиторий:** https://github.com/aruxojuyu665/EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES

**Ветка:** RAG-Milvus-Manus-Edition

**Документация:**
- `README.md` - общая информация
- `docs/SYSTEM_ARCHITECTURE.md` - архитектура системы
- `docs/RUNPOD_REQUIREMENTS.md` - требования к серверу
- `TESTING_REPORT.md` - результаты тестирования

---

**Дата создания:** 30 октября 2025  
**Версия документа:** 1.0  
**Автор:** Команда разработки RAG системы

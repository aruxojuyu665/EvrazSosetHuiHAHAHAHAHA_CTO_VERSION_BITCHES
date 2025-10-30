#!/bin/bash

###############################################################################
# Скрипт автоматического развертывания RAG системы на RunPod
# Версия: 1.0
# Дата: 30 октября 2025
###############################################################################

set -e  # Остановить при ошибке

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Функция для проверки успешности команды
check_status() {
    if [ $? -eq 0 ]; then
        log_info "$1 - OK"
    else
        log_error "$1 - FAILED"
        exit 1
    fi
}

###############################################################################
# Шаг 1: Проверка окружения
###############################################################################

log_info "========================================="
log_info "Шаг 1: Проверка окружения"
log_info "========================================="

# Проверка ОС
if [ -f /etc/os-release ]; then
    . /etc/os-release
    log_info "ОС: $NAME $VERSION"
else
    log_error "Невозможно определить ОС"
    exit 1
fi

# Проверка прав root
if [ "$EUID" -ne 0 ]; then 
    log_error "Скрипт должен запускаться от root"
    exit 1
fi

log_info "Проверка окружения завершена"

###############################################################################
# Шаг 2: Обновление системы
###############################################################################

log_info "========================================="
log_info "Шаг 2: Обновление системы"
log_info "========================================="

log_info "Обновление списка пакетов..."
apt update -qq
check_status "apt update"

log_info "Установка базовых утилит..."
apt install -y -qq \
    curl \
    wget \
    git \
    vim \
    htop \
    net-tools \
    build-essential \
    ca-certificates \
    gnupg \
    lsb-release > /dev/null 2>&1
check_status "Установка базовых утилит"

###############################################################################
# Шаг 3: Установка Docker
###############################################################################

log_info "========================================="
log_info "Шаг 3: Установка Docker"
log_info "========================================="

if command -v docker &> /dev/null; then
    log_warn "Docker уже установлен: $(docker --version)"
else
    log_info "Установка Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh > /dev/null 2>&1
    rm get-docker.sh
    check_status "Установка Docker"
fi

log_info "Запуск Docker..."
systemctl start docker
systemctl enable docker > /dev/null 2>&1
check_status "Запуск Docker"

log_info "Docker версия: $(docker --version)"

###############################################################################
# Шаг 4: Установка Docker Compose
###############################################################################

log_info "========================================="
log_info "Шаг 4: Установка Docker Compose"
log_info "========================================="

if command -v docker-compose &> /dev/null; then
    log_warn "Docker Compose уже установлен: $(docker-compose --version)"
else
    log_info "Установка Docker Compose..."
    apt install -y -qq docker-compose > /dev/null 2>&1
    check_status "Установка Docker Compose"
fi

log_info "Docker Compose версия: $(docker-compose --version)"

###############################################################################
# Шаг 5: Клонирование репозитория
###############################################################################

log_info "========================================="
log_info "Шаг 5: Клонирование репозитория"
log_info "========================================="

REPO_URL="https://github.com/aruxojuyu665/EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES.git"
REPO_DIR="/root/EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES"
BRANCH="RAG-Milvus-Manus-Edition"

if [ -d "$REPO_DIR" ]; then
    log_warn "Директория $REPO_DIR уже существует"
    log_info "Обновление репозитория..."
    cd "$REPO_DIR"
    git pull origin "$BRANCH"
    check_status "Обновление репозитория"
else
    log_info "Клонирование репозитория..."
    git clone -b "$BRANCH" "$REPO_URL" "$REPO_DIR"
    check_status "Клонирование репозитория"
    cd "$REPO_DIR"
fi

log_info "Текущая ветка: $(git branch --show-current)"

###############################################################################
# Шаг 6: Настройка переменных окружения
###############################################################################

log_info "========================================="
log_info "Шаг 6: Настройка переменных окружения"
log_info "========================================="

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        log_info "Создание .env из .env.example..."
        cp .env.example .env
        
        log_warn "ВАЖНО: Необходимо настроить API ключи в файле .env"
        log_warn "Откройте файл: vim $REPO_DIR/.env"
        log_warn ""
        log_warn "Обязательные параметры:"
        log_warn "  - OPENROUTER_API_KEY"
        log_warn "  - EMBEDDING_API_KEY"
        log_warn "  - MINIO_ACCESS_KEY (сгенерировать: openssl rand -base64 32)"
        log_warn "  - MINIO_SECRET_KEY (сгенерировать: openssl rand -base64 32)"
        log_warn ""
        
        read -p "Нажмите Enter после настройки .env файла..."
    else
        log_error ".env.example не найден"
        exit 1
    fi
else
    log_warn ".env файл уже существует"
fi

# Проверка наличия критических переменных
if grep -q "your_openrouter_api_key_here" .env; then
    log_error "OPENROUTER_API_KEY не настроен в .env"
    exit 1
fi

if grep -q "your_openai_api_key_for_embeddings" .env; then
    log_error "EMBEDDING_API_KEY не настроен в .env"
    exit 1
fi

log_info "Переменные окружения настроены"

###############################################################################
# Шаг 7: Создание необходимых директорий
###############################################################################

log_info "========================================="
log_info "Шаг 7: Создание директорий"
log_info "========================================="

mkdir -p data/raw data/processed output logs backups
check_status "Создание директорий"

###############################################################################
# Шаг 8: Запуск системы
###############################################################################

log_info "========================================="
log_info "Шаг 8: Запуск системы"
log_info "========================================="

log_info "Остановка существующих контейнеров..."
docker-compose down > /dev/null 2>&1 || true

log_info "Запуск сервисов..."
docker-compose up -d
check_status "Запуск сервисов"

log_info "Ожидание запуска сервисов (30 секунд)..."
sleep 30

###############################################################################
# Шаг 9: Проверка работоспособности
###############################################################################

log_info "========================================="
log_info "Шаг 9: Проверка работоспособности"
log_info "========================================="

log_info "Статус контейнеров:"
docker-compose ps

log_info "Проверка подключения к Milvus..."
docker-compose exec -T rag-app python3 -c "from pymilvus import connections; connections.connect(host='milvus-standalone', port='19530'); print('Milvus OK')" 2>/dev/null
check_status "Подключение к Milvus"

###############################################################################
# Шаг 10: Настройка автозапуска
###############################################################################

log_info "========================================="
log_info "Шаг 10: Настройка автозапуска"
log_info "========================================="

SERVICE_FILE="/etc/systemd/system/rag-system.service"

if [ -f "$SERVICE_FILE" ]; then
    log_warn "Systemd service уже существует"
else
    log_info "Создание systemd service..."
    cat > "$SERVICE_FILE" << EOF
[Unit]
Description=RAG System for GOST Analysis
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$REPO_DIR
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload
    systemctl enable rag-system.service > /dev/null 2>&1
    check_status "Настройка автозапуска"
fi

###############################################################################
# Завершение
###############################################################################

log_info "========================================="
log_info "Развертывание завершено успешно!"
log_info "========================================="

echo ""
log_info "Следующие шаги:"
echo "  1. Проверить логи: docker-compose logs -f"
echo "  2. Индексировать документы: docker-compose exec rag-app python -m src.main index --input /app/data/raw --create-new"
echo "  3. Проверить статистику: docker-compose exec rag-app python -m src.main stats"
echo "  4. Выполнить тестовый запрос: docker-compose exec rag-app python -m src.main query --question 'Тест'"
echo ""

log_info "Полезные команды:"
echo "  - Статус: docker-compose ps"
echo "  - Логи: docker-compose logs -f"
echo "  - Остановка: docker-compose down"
echo "  - Перезапуск: docker-compose restart"
echo "  - Обновление: cd $REPO_DIR && git pull && docker-compose up -d --build"
echo ""

log_info "Документация: $REPO_DIR/docs/"
log_info "Готово! 🚀"

"""
Конфигурация для RAG системы
Обновлено для поддержки Milvus Lite
"""

import os
import logging
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()


def _safe_int(env_var: str, default: int) -> int:
    """Безопасное получение int из переменной окружения"""
    try:
        return int(os.getenv(env_var, str(default)))
    except (ValueError, TypeError):
        return default


def _safe_float(env_var: str, default: float) -> float:
    """Безопасное получение float из переменной окружения"""
    try:
        return float(os.getenv(env_var, str(default)))
    except (ValueError, TypeError):
        return default


class OpenRouterConfig(BaseModel):
    """Конфигурация OpenRouter API"""
    api_key: str = Field(default_factory=lambda: os.getenv("OPENROUTER_API_KEY", ""))
    base_url: str = Field(default_factory=lambda: os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"))
    model: str = Field(default_factory=lambda: os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet"))
    temperature: float = Field(default_factory=lambda: _safe_float("TEMPERATURE", 0.1))
    max_tokens: int = Field(default_factory=lambda: _safe_int("MAX_TOKENS", 4096))


class EmbeddingConfig(BaseModel):
    """Конфигурация для embedding модели"""
    # Тип эмбеддингов: 'local' или 'openai'
    embedding_type: str = Field(default_factory=lambda: os.getenv("EMBEDDING_TYPE", "local"))
    
    # Настройки для локальных эмбеддингов
    local_model: str = Field(default_factory=lambda: os.getenv("LOCAL_EMBEDDING_MODEL", "intfloat/multilingual-e5-large"))
    local_device: str = Field(default_factory=lambda: os.getenv("LOCAL_EMBEDDING_DEVICE", "cuda"))
    local_batch_size: int = Field(default_factory=lambda: _safe_int("LOCAL_EMBEDDING_BATCH_SIZE", 32))
    
    # Настройки для OpenAI эмбеддингов
    model: str = Field(default_factory=lambda: os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"))
    api_key: str = Field(default_factory=lambda: os.getenv("EMBEDDING_API_KEY", ""))


class MilvusConfig(BaseModel):
    """
    Конфигурация Milvus Lite
    
    Обновлено для использования uri вместо host/port
    """
    # Новый параметр для Milvus Lite
    # Используем APP_MILVUS_URI чтобы избежать конфликта с pymilvus
    uri: str = Field(default_factory=lambda: os.getenv("APP_MILVUS_URI", "./milvus_lite.db"))
    
    # Старые параметры для обратной совместимости (deprecated)
    host: Optional[str] = Field(default_factory=lambda: os.getenv("MILVUS_HOST", None))
    port: Optional[int] = Field(default_factory=lambda: _safe_int("MILVUS_PORT", 0) if os.getenv("MILVUS_PORT") else None)
    
    # Общие параметры
    collection_name: str = Field(default_factory=lambda: os.getenv("MILVUS_COLLECTION_NAME", "gost_documents"))
    dimension: int = Field(default_factory=lambda: _safe_int("MILVUS_DIMENSION", 1024))
    metric_type: str = Field(default_factory=lambda: os.getenv("MILVUS_METRIC_TYPE", "COSINE"))


class RAGConfig(BaseModel):
    """Конфигурация RAG системы"""
    chunk_size: int = Field(default_factory=lambda: _safe_int("CHUNK_SIZE", 1000))
    chunk_overlap: int = Field(default_factory=lambda: _safe_int("CHUNK_OVERLAP", 200))
    top_k: int = Field(default_factory=lambda: _safe_int("TOP_K_RESULTS", 5))


class PathConfig(BaseModel):
    """Конфигурация путей"""
    project_root: Path = Field(default_factory=lambda: Path(__file__).parent.parent)
    data_raw: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "data" / "raw")
    data_processed: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "data" / "processed")


class Config(BaseModel):
    """Главная конфигурация приложения"""
    openrouter: OpenRouterConfig = Field(default_factory=OpenRouterConfig)
    embedding: EmbeddingConfig = Field(default_factory=EmbeddingConfig)
    milvus: MilvusConfig = Field(default_factory=MilvusConfig)
    rag: RAGConfig = Field(default_factory=RAGConfig)
    paths: PathConfig = Field(default_factory=PathConfig)

    def validate_config(self) -> bool:
        """
        Проверка конфигурации
        
        Returns:
            True если конфигурация валидна
            
        Raises:
            ValueError: Если обязательные параметры не установлены
        """
        logger = logging.getLogger(__name__)
        
        # Проверка OpenRouter API ключа
        if not self.openrouter.api_key:
            logger.error("Ошибка конфигурации: OPENROUTER_API_KEY не установлен")
            raise ValueError("OPENROUTER_API_KEY не установлен")
        
        # Проверка embedding API ключа только для типа 'openai'
        if self.embedding.embedding_type.lower() == "openai" and not self.embedding.api_key:
            logger.error("Ошибка конфигурации: EMBEDDING_API_KEY не установлен для типа 'openai'")
            raise ValueError("EMBEDDING_API_KEY не установлен для типа 'openai'")
        
        # Проверка Milvus конфигурации
        if not self.milvus.uri:
            logger.error("Ошибка конфигурации: MILVUS_URI не установлен")
            raise ValueError("MILVUS_URI не установлен")
        
        # Предупреждение о deprecated параметрах
        if self.milvus.host or self.milvus.port:
            logger.warning(
                "ВНИМАНИЕ: Параметры MILVUS_HOST и MILVUS_PORT устарели. "
                "Используйте MILVUS_URI для Milvus Lite"
            )
        
        logger.info("Конфигурация успешно валидирована")
        logger.info(f"Milvus URI: {self.milvus.uri}")
        logger.info(f"Embedding type: {self.embedding.embedding_type}")
        logger.info(f"LLM model: {self.openrouter.model}")
        
        return True


# Глобальный экземпляр конфигурации
config = Config()

"""
Конфигурация для RAG системы
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
    model: str = Field(default_factory=lambda: os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"))
    api_key: str = Field(default_factory=lambda: os.getenv("EMBEDDING_API_KEY", ""))


class MilvusConfig(BaseModel):
    """Конфигурация Milvus"""
    host: str = Field(default_factory=lambda: os.getenv("MILVUS_HOST", "localhost"))
    port: int = Field(default_factory=lambda: _safe_int("MILVUS_PORT", 19530))
    collection_name: str = Field(default_factory=lambda: os.getenv("MILVUS_COLLECTION_NAME", "gost_documents"))


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
        
        if not self.openrouter.api_key:
            logger.error("Ошибка конфигурации: OPENROUTER_API_KEY не установлен")
            raise ValueError("OPENROUTER_API_KEY не установлен")
        
        if not self.embedding.api_key:
            logger.error("Ошибка конфигурации: EMBEDDING_API_KEY не установлен")
            raise ValueError("EMBEDDING_API_KEY не установлен")
        
        logger.info("Конфигурация успешно валидирована")
        return True


# Глобальный экземпляр конфигурации
config = Config()

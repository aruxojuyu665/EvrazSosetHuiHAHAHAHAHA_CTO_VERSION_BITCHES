"""
Тесты для модуля конфигурации
"""

import pytest
import os
from unittest.mock import patch
from src.config import Config, _safe_int, _safe_float


def test_safe_int_valid():
    """Тест безопасного преобразования валидного int"""
    with patch.dict(os.environ, {"TEST_VAR": "42"}):
        result = _safe_int("TEST_VAR", 10)
        assert result == 42


def test_safe_int_invalid():
    """Тест безопасного преобразования невалидного int"""
    with patch.dict(os.environ, {"TEST_VAR": "invalid"}):
        result = _safe_int("TEST_VAR", 10)
        assert result == 10


def test_safe_int_missing():
    """Тест безопасного преобразования отсутствующей переменной"""
    result = _safe_int("NONEXISTENT_VAR", 10)
    assert result == 10


def test_safe_float_valid():
    """Тест безопасного преобразования валидного float"""
    with patch.dict(os.environ, {"TEST_VAR": "3.14"}):
        result = _safe_float("TEST_VAR", 1.0)
        assert result == 3.14


def test_safe_float_invalid():
    """Тест безопасного преобразования невалидного float"""
    with patch.dict(os.environ, {"TEST_VAR": "invalid"}):
        result = _safe_float("TEST_VAR", 1.0)
        assert result == 1.0


def test_config_validation_missing_openrouter_key():
    """Тест валидации конфигурации без OpenRouter API key"""
    with patch.dict(os.environ, {"OPENROUTER_API_KEY": "", "EMBEDDING_API_KEY": "test"}):
        config = Config()
        with pytest.raises(ValueError, match="OPENROUTER_API_KEY"):
            config.validate_config()


def test_config_validation_missing_embedding_key():
    """Тест валидации конфигурации без Embedding API key"""
    with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test", "EMBEDDING_API_KEY": ""}):
        config = Config()
        with pytest.raises(ValueError, match="EMBEDDING_API_KEY"):
            config.validate_config()


def test_config_validation_success():
    """Тест успешной валидации конфигурации"""
    with patch.dict(os.environ, {
        "OPENROUTER_API_KEY": "test_key",
        "EMBEDDING_API_KEY": "test_key"
    }):
        config = Config()
        assert config.validate_config() is True


def test_config_default_values():
    """Тест значений по умолчанию в конфигурации"""
    with patch.dict(os.environ, {}, clear=True):
        config = Config()
        assert config.milvus.host == "localhost"
        assert config.milvus.port == 19530
        assert config.rag.chunk_size == 1000
        assert config.rag.chunk_overlap == 200
        assert config.rag.top_k == 5
        assert config.openrouter.temperature == 0.1
        assert config.openrouter.max_tokens == 4096

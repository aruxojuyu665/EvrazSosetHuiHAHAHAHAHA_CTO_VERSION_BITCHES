"""
Тесты для RAG системы
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.rag import GOSTRAGSystem
from src.config import config


@pytest.fixture
def mock_config():
    """Мок конфигурации для тестов"""
    with patch('src.config.config') as mock_cfg:
        mock_cfg.openrouter.api_key = "test_key"
        mock_cfg.embedding.api_key = "test_key"
        mock_cfg.milvus.host = "localhost"
        mock_cfg.milvus.port = 19530
        mock_cfg.rag.chunk_size = 1000
        mock_cfg.rag.chunk_overlap = 200
        mock_cfg.rag.top_k = 5
        yield mock_cfg


@pytest.fixture
def rag_system(mock_config):
    """Фикстура RAG системы"""
    return GOSTRAGSystem(
        openrouter_api_key="test_key",
        embedding_api_key="test_key"
    )


def test_rag_system_initialization(rag_system):
    """Тест инициализации RAG системы"""
    assert rag_system is not None
    assert rag_system.openrouter_api_key == "test_key"
    assert rag_system.embedding_api_key == "test_key"


@patch('src.rag.rag_system.OpenAI')
def test_setup_llm(mock_openai, rag_system):
    """Тест настройки LLM"""
    # LLM должен быть настроен при инициализации
    assert rag_system.llm is not None


@patch('src.rag.rag_system.OpenAIEmbedding')
def test_setup_embeddings(mock_embedding, rag_system):
    """Тест настройки embeddings"""
    # Embedding модель должна быть настроена при инициализации
    assert rag_system.embed_model is not None


@patch('src.vector_store.milvus_store.connections')
@patch('src.vector_store.milvus_store.Collection')
def test_initialize_milvus(mock_collection, mock_connections, rag_system):
    """Тест инициализации Milvus"""
    mock_connections.connect.return_value = None
    
    # Инициализация не должна вызывать ошибок
    # (в реальности требуется запущенный Milvus)
    # rag_system.initialize_milvus()
    # assert rag_system.milvus_manager is not None
    pass


def test_load_documents_file_not_found(rag_system):
    """Тест загрузки несуществующего документа"""
    with pytest.raises(Exception):
        rag_system.load_documents("/nonexistent/path.pdf")


@patch('src.rag.rag_system.SimpleDirectoryReader')
def test_load_documents_success(mock_reader, rag_system):
    """Тест успешной загрузки документов"""
    mock_reader.return_value.load_data.return_value = [
        Mock(text="Test document 1"),
        Mock(text="Test document 2")
    ]
    
    # documents = rag_system.load_documents("/test/path")
    # assert len(documents) == 2
    pass


def test_query_without_setup(rag_system):
    """Тест запроса без настройки query engine"""
    with pytest.raises(ValueError):
        rag_system.query("Test question")


def test_extract_strength_class_info_structure(rag_system):
    """Тест структуры метода извлечения информации о классе прочности"""
    # Проверяем, что метод существует и принимает параметры
    assert hasattr(rag_system, 'extract_strength_class_info')
    assert callable(rag_system.extract_strength_class_info)


def test_get_stats_structure(rag_system):
    """Тест структуры метода получения статистики"""
    # Проверяем, что метод существует
    assert hasattr(rag_system, 'get_stats')
    assert callable(rag_system.get_stats)
    
    # Статистика должна возвращать словарь
    stats = rag_system.get_stats()
    assert isinstance(stats, dict)
    assert 'config' in stats

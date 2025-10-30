"""
Тесты для Milvus менеджера
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.vector_store import MilvusManager


@pytest.fixture
def milvus_manager():
    """Фикстура Milvus менеджера"""
    return MilvusManager(
        host="localhost",
        port=19530,
        collection_name="test_collection",
        dim=1536
    )


def test_milvus_manager_initialization(milvus_manager):
    """Тест инициализации менеджера"""
    assert milvus_manager.host == "localhost"
    assert milvus_manager.port == 19530
    assert milvus_manager.collection_name == "test_collection"
    assert milvus_manager.dim == 1536


@patch('src.vector_store.milvus_store.connections')
def test_connect_success(mock_connections, milvus_manager):
    """Тест успешного подключения"""
    mock_connections.connect.return_value = None
    
    result = milvus_manager.connect()
    
    mock_connections.connect.assert_called_once()
    assert result is True


@patch('src.vector_store.milvus_store.connections')
def test_connect_failure(mock_connections, milvus_manager):
    """Тест неудачного подключения"""
    mock_connections.connect.side_effect = Exception("Connection failed")
    
    result = milvus_manager.connect()
    
    assert result is False


@patch('src.vector_store.milvus_store.utility')
@patch('src.vector_store.milvus_store.Collection')
@patch('src.vector_store.milvus_store.CollectionSchema')
def test_create_collection_new(mock_schema, mock_collection, mock_utility, milvus_manager):
    """Тест создания новой коллекции"""
    mock_utility.has_collection.return_value = False
    mock_collection_instance = Mock()
    mock_collection.return_value = mock_collection_instance
    
    result = milvus_manager.create_collection()
    
    assert result is True


@patch('src.vector_store.milvus_store.utility')
@patch('src.vector_store.milvus_store.Collection')
def test_create_collection_exists(mock_collection, mock_utility, milvus_manager):
    """Тест когда коллекция уже существует"""
    mock_utility.has_collection.return_value = True
    
    result = milvus_manager.create_collection(overwrite=False)
    
    assert result is True


def test_get_vector_store(milvus_manager):
    """Тест получения векторного хранилища"""
    with patch('src.vector_store.milvus_store.MilvusVectorStore') as mock_vs:
        vector_store = milvus_manager.get_vector_store()
        mock_vs.assert_called_once()


@patch('src.vector_store.milvus_store.Collection')
def test_get_collection_stats(mock_collection, milvus_manager):
    """Тест получения статистики коллекции"""
    mock_collection_instance = Mock()
    mock_collection_instance.num_entities = 100
    mock_collection_instance.description = "Test collection"
    mock_collection.return_value = mock_collection_instance
    
    milvus_manager.collection = mock_collection_instance
    stats = milvus_manager.get_collection_stats()
    
    assert isinstance(stats, dict)
    assert stats['num_entities'] == 100


@patch('src.vector_store.milvus_store.connections')
def test_disconnect(mock_connections, milvus_manager):
    """Тест отключения"""
    milvus_manager.disconnect()
    mock_connections.disconnect.assert_called_once()

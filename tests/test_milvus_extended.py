"""
Расширенные тесты для Milvus менеджера
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.vector_store.milvus_store import MilvusManager
from src.config import config


@pytest.fixture
def milvus_manager():
    """Фикстура для создания MilvusManager"""
    return MilvusManager(
        host=config.milvus.host,
        port=config.milvus.port,
        collection_name="test_collection"
    )


class TestMilvusManagerContextManager:
    """Тесты context manager"""
    
    @patch('src.vector_store.milvus_store.connections')
    def test_context_manager_enter(self, mock_connections):
        """Тест входа в context manager"""
        mock_connections.connect.return_value = None
        
        with MilvusManager() as manager:
            assert manager is not None
            mock_connections.connect.assert_called_once()
    
    @patch('src.vector_store.milvus_store.connections')
    def test_context_manager_exit(self, mock_connections):
        """Тест выхода из context manager"""
        mock_connections.connect.return_value = None
        mock_connections.has_connection.return_value = True
        mock_connections.disconnect.return_value = None
        
        with MilvusManager() as manager:
            pass
        
        mock_connections.disconnect.assert_called_once()
    
    @patch('src.vector_store.milvus_store.connections')
    def test_context_manager_with_exception(self, mock_connections):
        """Тест context manager при исключении"""
        mock_connections.connect.return_value = None
        mock_connections.has_connection.return_value = True
        mock_connections.disconnect.return_value = None
        
        with pytest.raises(ValueError):
            with MilvusManager() as manager:
                raise ValueError("Test error")
        
        # disconnect должен быть вызван даже при исключении
        mock_connections.disconnect.assert_called_once()


class TestMilvusManagerConnectionCheck:
    """Тесты проверки подключения"""
    
    @patch('src.vector_store.milvus_store.connections')
    def test_is_connected_true(self, mock_connections, milvus_manager):
        """Тест проверки подключения когда подключено"""
        mock_connections.has_connection.return_value = True
        
        assert milvus_manager._is_connected() is True
    
    @patch('src.vector_store.milvus_store.connections')
    def test_is_connected_false(self, mock_connections, milvus_manager):
        """Тест проверки подключения когда не подключено"""
        mock_connections.has_connection.return_value = False
        
        assert milvus_manager._is_connected() is False
    
    @patch('src.vector_store.milvus_store.connections')
    def test_is_connected_exception(self, mock_connections, milvus_manager):
        """Тест проверки подключения при исключении"""
        mock_connections.has_connection.side_effect = Exception("Error")
        
        assert milvus_manager._is_connected() is False
    
    @patch('src.vector_store.milvus_store.utility')
    @patch('src.vector_store.milvus_store.connections')
    def test_auto_reconnect_on_operation(self, mock_connections, mock_utility, milvus_manager):
        """Тест автоматического переподключения при операции"""
        # Сначала не подключено, потом подключено
        mock_connections.has_connection.side_effect = [False, True]
        mock_connections.connect.return_value = None
        mock_utility.has_collection.return_value = True
        
        result = milvus_manager.collection_exists()
        
        # Должно автоматически переподключиться
        mock_connections.connect.assert_called_once()
        assert result is True


class TestMilvusManagerLoadCollection:
    """Тесты загрузки коллекции"""
    
    @patch('src.vector_store.milvus_store.Collection')
    @patch('src.vector_store.milvus_store.connections')
    def test_load_collection_success(self, mock_connections, mock_collection_class, milvus_manager):
        """Тест успешной загрузки коллекции"""
        mock_connections.has_connection.return_value = True
        mock_collection = MagicMock()
        mock_collection_class.return_value = mock_collection
        
        milvus_manager.load_collection()
        
        mock_collection.load.assert_called_once()
    
    @patch('src.vector_store.milvus_store.Collection')
    @patch('src.vector_store.milvus_store.connections')
    def test_load_collection_not_connected(self, mock_connections, mock_collection_class, milvus_manager):
        """Тест загрузки коллекции без подключения"""
        mock_connections.has_connection.side_effect = [False, True]
        mock_connections.connect.return_value = None
        mock_collection = MagicMock()
        mock_collection_class.return_value = mock_collection
        
        milvus_manager.load_collection()
        
        # Должно автоматически подключиться
        mock_connections.connect.assert_called_once()
        mock_collection.load.assert_called_once()


class TestMilvusManagerErrorHandling:
    """Тесты обработки ошибок"""
    
    @patch('src.vector_store.milvus_store.connections')
    def test_disconnect_when_not_connected(self, mock_connections, milvus_manager):
        """Тест отключения когда нет подключения"""
        mock_connections.has_connection.return_value = False
        
        # Не должно выбросить исключение
        milvus_manager.disconnect()
        
        # disconnect не должен вызываться
        mock_connections.disconnect.assert_not_called()
    
    @patch('src.vector_store.milvus_store.connections')
    def test_connect_with_invalid_params(self, mock_connections):
        """Тест подключения с невалидными параметрами"""
        mock_connections.connect.side_effect = Exception("Invalid parameters")
        manager = MilvusManager(host="invalid_host", port=-1)
        
        with pytest.raises(Exception, match="Invalid parameters"):
            manager.connect()

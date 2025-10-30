"""
Модуль для работы с Milvus векторной базой данных
"""

import logging
from typing import List, Dict, Optional
from pymilvus import (
    connections,
    Collection,
    CollectionSchema,
    FieldSchema,
    DataType,
    utility
)
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.core import VectorStoreIndex, StorageContext

logger = logging.getLogger(__name__)


class MilvusManager:
    """Менеджер для работы с Milvus"""
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
        return False
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 19530,
        collection_name: str = "gost_documents",
        dim: int = 1536  # Размерность для text-embedding-3-small
    ):
        """
        Инициализация менеджера Milvus
        
        Args:
            host: Хост Milvus
            port: Порт Milvus
            collection_name: Имя коллекции
            dim: Размерность векторов
        """
        self.host = host
        self.port = port
        self.collection_name = collection_name
        self.dim = dim
        self.collection: Optional[Collection] = None
        
    def connect(self) -> bool:
        """
        Подключение к Milvus
        
        Returns:
            True если подключение успешно
        """
        try:
            connections.connect(
                alias="default",
                host=self.host,
                port=self.port
            )
            logger.info(f"Подключено к Milvus: {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Ошибка подключения к Milvus: {e}")
            return False
    
    def create_collection(self, overwrite: bool = False) -> bool:
        """
        Создание коллекции в Milvus
        
        Args:
            overwrite: Перезаписать существующую коллекцию
            
        Returns:
            True если коллекция создана успешно
        """
        try:
            # Проверка существования коллекции
            if utility.has_collection(self.collection_name):
                if overwrite:
                    utility.drop_collection(self.collection_name)
                    logger.info(f"Коллекция {self.collection_name} удалена")
                else:
                    logger.info(f"Коллекция {self.collection_name} уже существует")
                    self.collection = Collection(self.collection_name)
                    return True
            
            # Определение схемы коллекции
            fields = [
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self.dim),
                FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(name="metadata", dtype=DataType.VARCHAR, max_length=65535)
            ]
            
            schema = CollectionSchema(
                fields=fields,
                description="GOST documents collection"
            )
            
            # Создание коллекции
            self.collection = Collection(
                name=self.collection_name,
                schema=schema
            )
            
            # Создание индекса для векторного поиска
            index_params = {
                "metric_type": "L2",
                "index_type": "IVF_FLAT",
                "params": {"nlist": 1024}
            }
            
            self.collection.create_index(
                field_name="embedding",
                index_params=index_params
            )
            
            logger.info(f"Коллекция {self.collection_name} создана успешно")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка создания коллекции: {e}")
            return False
    
    def get_vector_store(self) -> MilvusVectorStore:
        """
        Получение векторного хранилища для LlamaIndex
        
        Returns:
            MilvusVectorStore объект
        """
        vector_store = MilvusVectorStore(
            host=self.host,
            port=self.port,
            collection_name=self.collection_name,
            dim=self.dim
        )
        return vector_store
    
    def load_collection(self) -> bool:
        """
        Загрузка коллекции в память
        
        Returns:
            True если загрузка успешна
        """
        try:
            # Проверка подключения
            if not self._is_connected():
                logger.warning("Нет подключения к Milvus, попытка переподключения")
                if not self.connect():
                    return False
            
            if self.collection is None:
                self.collection = Collection(self.collection_name)
            
            self.collection.load()
            logger.info(f"Коллекция {self.collection_name} загружена в память")
            return True
        except Exception as e:
            logger.error(f"Ошибка загрузки коллекции: {e}")
            return False
    
    def get_collection_stats(self) -> Dict:
        """
        Получение статистики коллекции
        
        Returns:
            Словарь со статистикой
        """
        try:
            # Проверка подключения
            if not self._is_connected():
                logger.warning("Нет подключения к Milvus, попытка переподключения")
                if not self.connect():
                    return {}
            
            if self.collection is None:
                self.collection = Collection(self.collection_name)
            
            stats = {
                "name": self.collection_name,
                "num_entities": self.collection.num_entities,
                "description": self.collection.description
            }
            return stats
        except Exception as e:
            logger.error(f"Ошибка получения статистики: {e}")
            return {}
    
    def _is_connected(self) -> bool:
        """
        Проверка подключения к Milvus
        
        Returns:
            True если подключение активно
        """
        try:
            return connections.has_connection("default")
        except Exception:
            return False
    
    def disconnect(self) -> None:
        """
        Отключение от Milvus
        
        Returns:
            None
        """
        try:
            if self._is_connected():
                connections.disconnect(alias="default")
                logger.info("Отключено от Milvus")
        except Exception as e:
            logger.error(f"Ошибка отключения от Milvus: {e}")

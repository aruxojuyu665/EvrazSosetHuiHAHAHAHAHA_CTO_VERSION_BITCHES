"""
Модуль для работы с Milvus Lite векторной базой данных
Обновлено для использования Milvus Lite вместо Milvus Standalone
"""

import logging
from typing import List, Dict, Optional
from pymilvus import MilvusClient
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.core import VectorStoreIndex, StorageContext

logger = logging.getLogger(__name__)


class MilvusManager:
    """Менеджер для работы с Milvus Lite"""
    
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
        uri: str = "./milvus_lite.db",
        collection_name: str = "gost_documents",
        dim: int = 1024,  # Размерность для intfloat/multilingual-e5-large
        metric_type: str = "COSINE"
    ):
        """
        Инициализация менеджера Milvus Lite
        
        Args:
            uri: Путь к файлу базы данных Milvus Lite
            collection_name: Имя коллекции
            dim: Размерность векторов
            metric_type: Тип метрики (COSINE, L2, IP)
        """
        self.uri = uri
        self.collection_name = collection_name
        self.dim = dim
        self.metric_type = metric_type
        self.client: Optional[MilvusClient] = None
        
    def connect(self) -> bool:
        """
        Подключение к Milvus Lite
        
        Returns:
            True если подключение успешно
        """
        try:
            self.client = MilvusClient(uri=self.uri)
            logger.info(f"Подключено к Milvus Lite: {self.uri}")
            return True
        except Exception as e:
            logger.error(f"Ошибка подключения к Milvus Lite: {e}")
            return False
    
    def create_collection(self, overwrite: bool = False) -> bool:
        """
        Создание коллекции в Milvus Lite
        
        Args:
            overwrite: Перезаписать существующую коллекцию
            
        Returns:
            True если коллекция создана успешно
        """
        try:
            if self.client is None:
                logger.error("Клиент не подключен. Вызовите connect() сначала")
                return False
            
            # Проверка существования коллекции
            collections = self.client.list_collections()
            collection_exists = self.collection_name in collections
            
            if collection_exists:
                if overwrite:
                    self.client.drop_collection(collection_name=self.collection_name)
                    logger.info(f"Коллекция {self.collection_name} удалена")
                else:
                    logger.info(f"Коллекция {self.collection_name} уже существует")
                    return True
            
            # Создание коллекции с автоматической схемой
            # auto_id=False для совместимости с LlamaIndex (использует строковые ID)
            self.client.create_collection(
                collection_name=self.collection_name,
                dimension=self.dim,
                metric_type=self.metric_type,
                auto_id=False,
                id_type="string",
                max_length=65535
            )
            
            logger.info(f"Коллекция {self.collection_name} создана успешно")
            logger.info(f"Параметры: dimension={self.dim}, metric_type={self.metric_type}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка создания коллекции: {e}")
            return False
    
    def get_vector_store(self, overwrite: bool = False) -> MilvusVectorStore:
        """
        Получение векторного хранилища для LlamaIndex
        
        Args:
            overwrite: Перезаписать существующую коллекцию
        
        Returns:
            MilvusVectorStore объект
        """
        try:
            # LlamaIndex MilvusVectorStore поддерживает Milvus Lite через uri параметр
            # Позволяем MilvusVectorStore самому управлять схемой коллекции
            vector_store = MilvusVectorStore(
                uri=self.uri,
                collection_name=self.collection_name,
                dim=self.dim,
                overwrite=overwrite
            )
            logger.info(f"Векторное хранилище создано для коллекции {self.collection_name}")
            return vector_store
        except Exception as e:
            logger.error(f"Ошибка создания векторного хранилища: {e}")
            raise
    
    def load_collection(self) -> bool:
        """
        Загрузка коллекции в память
        
        Note:
            В Milvus Lite коллекции автоматически доступны,
            явная загрузка не требуется
        
        Returns:
            True если коллекция доступна
        """
        try:
            if self.client is None:
                logger.warning("Клиент не подключен, попытка переподключения")
                if not self.connect():
                    return False
            
            collections = self.client.list_collections()
            if self.collection_name in collections:
                logger.info(f"Коллекция {self.collection_name} доступна")
                return True
            else:
                logger.warning(f"Коллекция {self.collection_name} не найдена")
                return False
                
        except Exception as e:
            logger.error(f"Ошибка проверки коллекции: {e}")
            return False
    
    def get_collection_stats(self) -> Dict:
        """
        Получение статистики коллекции
        
        Returns:
            Словарь со статистикой
        """
        try:
            if self.client is None:
                logger.warning("Клиент не подключен, попытка переподключения")
                if not self.connect():
                    return {"error": "Не удалось подключиться к Milvus Lite"}
            
            # Проверка существования коллекции
            collections = self.client.list_collections()
            if self.collection_name not in collections:
                logger.warning(f"Коллекция {self.collection_name} не найдена")
                return {
                    "name": self.collection_name,
                    "exists": False,
                    "num_entities": 0
                }
            
            # Безопасное получение статистики
            try:
                stats = self.client.get_collection_stats(collection_name=self.collection_name)
                row_count = stats.get("row_count", 0)
            except Exception as e:
                logger.warning(f"Не удалось получить статистику: {e}")
                row_count = 0
            
            result = {
                "name": self.collection_name,
                "exists": True,
                "num_entities": row_count,
                "dimension": self.dim,
                "metric_type": self.metric_type
            }
            
            logger.info(f"Статистика коллекции {self.collection_name}: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Ошибка получения статистики: {e}")
            return {
                "name": self.collection_name,
                "error": str(e)
            }
    
    def insert_data(self, data: List[Dict]) -> bool:
        """
        Вставка данных в коллекцию
        
        Args:
            data: Список словарей с данными для вставки
                  Каждый словарь должен содержать ключи: vector, text, metadata
        
        Returns:
            True если вставка успешна
        """
        try:
            if self.client is None:
                logger.error("Клиент не подключен")
                return False
            
            if not data:
                logger.warning("Нет данных для вставки")
                return False
            
            # Валидация размерности векторов
            for i, item in enumerate(data):
                if "vector" in item:
                    vector_dim = len(item["vector"])
                    if vector_dim != self.dim:
                        logger.error(
                            f"Неверная размерность вектора в записи {i}: "
                            f"ожидается {self.dim}, получено {vector_dim}"
                        )
                        return False
            
            # Вставка данных
            self.client.insert(
                collection_name=self.collection_name,
                data=data
            )
            
            logger.info(f"Вставлено {len(data)} записей в коллекцию {self.collection_name}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка вставки данных: {e}")
            return False
    
    def search(
        self,
        query_vector: List[float],
        limit: int = 5,
        output_fields: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Поиск похожих векторов
        
        Args:
            query_vector: Вектор запроса
            limit: Количество результатов
            output_fields: Поля для возврата
        
        Returns:
            Список найденных результатов
        """
        try:
            if self.client is None:
                logger.error("Клиент не подключен")
                return []
            
            # Поиск
            results = self.client.search(
                collection_name=self.collection_name,
                data=[query_vector],
                limit=limit,
                output_fields=output_fields or ["text", "metadata"]
            )
            
            logger.info(f"Найдено {len(results[0]) if results else 0} результатов")
            return results[0] if results else []
            
        except Exception as e:
            logger.error(f"Ошибка поиска: {e}")
            return []
    
    def _is_connected(self) -> bool:
        """
        Проверка подключения к Milvus Lite
        
        Returns:
            True если подключение активно
        """
        try:
            if self.client is None:
                return False
            # Проверка через получение списка коллекций
            self.client.list_collections()
            return True
        except Exception:
            return False
    
    def disconnect(self) -> None:
        """
        Отключение от Milvus Lite
        
        Note:
            В Milvus Lite явное отключение не требуется,
            клиент автоматически управляет соединением
        """
        try:
            if self.client is not None:
                self.client = None
                logger.info("Отключено от Milvus Lite")
        except Exception as e:
            logger.error(f"Ошибка отключения от Milvus Lite: {e}")

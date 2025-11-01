"""
RAG система на основе LlamaIndex с интеграцией OpenRouter и Milvus Lite
Обновлено для использования Milvus Lite вместо Milvus Standalone
"""

import logging
from typing import List, Dict, Optional
from pathlib import Path

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    Settings,
    PromptTemplate
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import get_response_synthesizer

from src.vector_store import MilvusManager
from src.config import config
from src.utils import retry_on_error

logger = logging.getLogger(__name__)


class GOSTRAGSystem:
    """RAG система для анализа документов ГОСТ"""
    
    def __init__(
        self,
        openrouter_api_key: Optional[str] = None,
        embedding_api_key: Optional[str] = None,
        milvus_uri: Optional[str] = None
    ):
        """
        Инициализация RAG системы
        
        Args:
            openrouter_api_key: API ключ OpenRouter
            embedding_api_key: API ключ для embeddings (только для типа 'openai')
            milvus_uri: URI для Milvus Lite (путь к файлу БД)
        """
        # Использование конфигурации
        self.openrouter_api_key = openrouter_api_key or config.openrouter.api_key
        self.embedding_api_key = embedding_api_key or config.embedding.api_key
        self.milvus_uri = milvus_uri or config.milvus.uri
        
        # Инициализация компонентов
        self.milvus_manager: Optional[MilvusManager] = None
        self.index: Optional[VectorStoreIndex] = None
        self.query_engine = None
        
        self._setup_llm()
        self._setup_embeddings()
        
    def _setup_llm(self):
        """Настройка LLM через OpenRouter"""
        try:
            # OpenRouter совместим с OpenAI API
            # Используем additional_kwargs для передачи реальной модели
            self.llm = OpenAI(
                api_key=self.openrouter_api_key,
                api_base=config.openrouter.base_url,
                model=config.openrouter.model,
                temperature=config.openrouter.temperature,
                max_tokens=config.openrouter.max_tokens,
                timeout=60.0,
                max_retries=2,
                default_headers={
                    "HTTP-Referer": "https://github.com/gost-rag-project",
                    "X-Title": "GOST RAG System"
                },
                logprobs=False,
                is_chat_model=True,
                is_function_calling_model=False
            )
            
            # Патчим metadata чтобы избежать проверки модели
            from llama_index.core.base.llms.types import LLMMetadata
            custom_metadata = LLMMetadata(
                context_window=200000,
                num_output=config.openrouter.max_tokens,
                is_chat_model=True,
                is_function_calling_model=False,
                model_name=config.openrouter.model
            )
            
            # Переопределяем metadata как property
            type(self.llm).metadata = property(lambda self: custom_metadata)
            
            # Установка глобальных настроек LlamaIndex
            Settings.llm = self.llm
            
            logger.info(f"LLM настроен: {config.openrouter.model}")
        except Exception as e:
            logger.error(f"Ошибка настройки LLM: {e}")
            raise
    
    def _setup_embeddings(self):
        """Настройка embedding модели"""
        try:
            embedding_type = config.embedding.embedding_type.lower()
            
            if embedding_type == "local":
                # Использование локальной модели
                from llama_index.embeddings.huggingface import HuggingFaceEmbedding
                
                logger.info(f"Инициализация локальной embedding модели: {config.embedding.local_model}")
                logger.info(f"Устройство: {config.embedding.local_device}")
                
                self.embed_model = HuggingFaceEmbedding(
                    model_name=config.embedding.local_model,
                    device=config.embedding.local_device,
                    embed_batch_size=config.embedding.local_batch_size
                )
                
                logger.info(f"Локальная embedding модель загружена: {config.embedding.local_model}")
                
            elif embedding_type == "openai":
                # Использование OpenAI API
                self.embed_model = OpenAIEmbedding(
                    api_key=self.embedding_api_key,
                    model=config.embedding.model,
                    timeout=30.0,
                    max_retries=2
                )
                
                logger.info(f"OpenAI embedding модель настроена: {config.embedding.model}")
                
            else:
                raise ValueError(f"Неизвестный тип эмбеддингов: {embedding_type}. Используйте 'local' или 'openai'")
            
            # Установка глобальных настроек
            Settings.embed_model = self.embed_model
            
        except Exception as e:
            logger.error(f"Ошибка настройки embeddings: {e}")
            raise
    
    def initialize_milvus(self, create_new: bool = False):
        """
        Инициализация Milvus Lite
        
        Args:
            create_new: Создать новую коллекцию (удалит существующую)
        """
        try:
            logger.info(f"Инициализация Milvus Lite с URI: {self.milvus_uri}")
            
            self.milvus_manager = MilvusManager(
                uri=self.milvus_uri,
                collection_name=config.milvus.collection_name,
                dim=config.milvus.dimension,
                metric_type=config.milvus.metric_type
            )
            
            if not self.milvus_manager.connect():
                raise ConnectionError("Не удалось подключиться к Milvus Lite")
            
            # Не создаем коллекцию вручную - позволяем LlamaIndex MilvusVectorStore управлять схемой
            # Сохраняем create_new для передачи в get_vector_store
            self._create_new = create_new
            
            logger.info("Milvus Lite инициализирован успешно")
        except Exception as e:
            logger.error(f"Ошибка инициализации Milvus Lite: {e}")
            raise
    
    def load_documents(self, document_path: str) -> List:
        """
        Загрузка документов из директории или файла
        
        Args:
            document_path: Путь к документу или директории
            
        Returns:
            Список загруженных документов
            
        Note:
            Для очень больших файлов (>100MB) рекомендуется использовать
            streaming или batch обработку для оптимизации памяти.
        """
        try:
            path = Path(document_path)
            
            if path.is_file():
                # Загрузка одного файла
                reader = SimpleDirectoryReader(
                    input_files=[str(path)]
                )
            else:
                # Загрузка всех файлов из директории
                reader = SimpleDirectoryReader(
                    input_dir=str(path)
                )
            
            documents = reader.load_data()
            logger.info(f"Загружено документов: {len(documents)}")
            return documents
            
        except Exception as e:
            logger.error(f"Ошибка загрузки документов: {e}")
            raise
    
    def create_index(self, documents: List, show_progress: bool = True):
        """
        Создание индекса из документов
        
        Args:
            documents: Список документов
            show_progress: Показывать прогресс
        """
        try:
            # Настройка парсера для разбиения на чанки
            text_splitter = SentenceSplitter(
                chunk_size=config.rag.chunk_size,
                chunk_overlap=config.rag.chunk_overlap
            )
            
            Settings.text_splitter = text_splitter
            
            # Получение векторного хранилища с передачей overwrite
            overwrite = getattr(self, '_create_new', False)
            vector_store = self.milvus_manager.get_vector_store(overwrite=overwrite)
            storage_context = StorageContext.from_defaults(
                vector_store=vector_store
            )
            
            logger.info("Создание индекса из документов...")
            logger.info(f"Chunk size: {config.rag.chunk_size}, overlap: {config.rag.chunk_overlap}")
            
            # Создание индекса
            self.index = VectorStoreIndex.from_documents(
                documents,
                storage_context=storage_context,
                show_progress=show_progress
            )
            
            logger.info("Индекс создан успешно")
            
        except Exception as e:
            logger.error(f"Ошибка создания индекса: {e}")
            raise
    
    def load_index(self):
        """Загрузка существующего индекса из Milvus Lite"""
        try:
            logger.info("Загрузка существующего индекса из Milvus Lite...")
            
            # Проверка существования коллекции
            if not self.milvus_manager.load_collection():
                raise ValueError(
                    f"Коллекция {config.milvus.collection_name} не найдена. "
                    "Сначала создайте индекс с помощью команды 'index'."
                )
            
            vector_store = self.milvus_manager.get_vector_store()
            storage_context = StorageContext.from_defaults(
                vector_store=vector_store
            )
            
            self.index = VectorStoreIndex.from_vector_store(
                vector_store=vector_store,
                storage_context=storage_context
            )
            
            logger.info("Индекс загружен из Milvus Lite")
            
        except Exception as e:
            logger.error(f"Ошибка загрузки индекса: {e}")
            raise
    
    def setup_query_engine(
        self,
        top_k: Optional[int] = None,
        custom_prompt: Optional[str] = None
    ):
        """
        Настройка query engine
        
        Args:
            top_k: Количество релевантных чанков для поиска
            custom_prompt: Кастомный промпт для генерации ответа
        """
        try:
            if self.index is None:
                raise ValueError("Индекс не создан. Вызовите create_index() или load_index()")
            
            top_k = top_k or config.rag.top_k
            
            logger.info(f"Настройка query engine с top_k={top_k}")
            
            # Создаем response_synthesizer вручную с кастомным LLM
            from llama_index.core.response_synthesizers import CompactAndRefine
            response_synthesizer = CompactAndRefine(
                llm=self.llm,
                streaming=False
            )
            
            # Используем as_query_engine() с явным response_synthesizer
            self.query_engine = self.index.as_query_engine(
                similarity_top_k=top_k,
                response_synthesizer=response_synthesizer
            )
            
            # Установка кастомного промпта если предоставлен
            if custom_prompt:
                qa_prompt = PromptTemplate(custom_prompt)
                self.query_engine.update_prompts(
                    {"response_synthesizer:text_qa_template": qa_prompt}
                )
            
            logger.info("Query engine настроен")
            
        except Exception as e:
            logger.error(f"Ошибка настройки query engine: {e}")
            raise
    
    @retry_on_error(max_retries=3, delay=2.0, backoff=2.0)
    def query(self, question: str) -> Dict:
        """
        Выполнение запроса к RAG системе
        
        Args:
            question: Вопрос
            
        Returns:
            Словарь с ответом и метаданными
        """
        try:
            if self.query_engine is None:
                raise ValueError("Query engine не настроен. Вызовите setup_query_engine()")
            
            logger.info(f"Выполнение запроса: {question[:100]}...")
            
            response = self.query_engine.query(question)
            
            result = {
                "answer": str(response),
                "source_nodes": [
                    {
                        "text": node.node.text,
                        "score": node.score,
                        "metadata": node.node.metadata
                    }
                    for node in response.source_nodes
                ]
            }
            
            logger.info(f"Запрос выполнен, найдено {len(result['source_nodes'])} источников")
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка выполнения запроса: {e}")
            raise
    
    def extract_strength_class_info(self, class_name: str = "C235") -> Dict:
        """
        Извлечение информации о классе прочности
        
        Args:
            class_name: Название класса прочности
            
        Returns:
            Словарь с информацией о классе прочности
        """
        prompt = f"""
        Извлеки всю доступную информацию о классе прочности стали {class_name} из документа ГОСТ 27772-2021.
        
        Необходимо найти и структурировать следующую информацию:
        1. Химический состав (массовая доля элементов в %)
        2. Механические свойства (предел текучести, временное сопротивление, относительное удлинение, ударная вязкость)
        3. Предельные отклонения
        4. Требования к испытаниям
        5. Информация о сортаменте и видах продукции
        6. Ссылки на другие стандарты, если они упоминаются в контексте {class_name}
        
        Представь информацию в структурированном виде с указанием конкретных значений и диапазонов.
        """
        
        logger.info(f"Извлечение информации о классе прочности: {class_name}")
        
        return self.query(prompt)
    
    def get_stats(self) -> Dict:
        """Получение статистики системы"""
        stats = {
            "milvus": self.milvus_manager.get_collection_stats() if self.milvus_manager else {},
            "config": {
                "model": config.openrouter.model,
                "embedding_type": config.embedding.embedding_type,
                "embedding_model": config.embedding.local_model if config.embedding.embedding_type == "local" else config.embedding.model,
                "chunk_size": config.rag.chunk_size,
                "chunk_overlap": config.rag.chunk_overlap,
                "top_k": config.rag.top_k,
                "milvus_uri": config.milvus.uri
            }
        }
        
        logger.info("Статистика системы получена")
        
        return stats

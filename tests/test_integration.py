"""
Интеграционные тесты RAG системы

Эти тесты требуют запущенного Milvus и настроенных API ключей.
Для запуска: pytest tests/test_integration.py --integration
"""

import pytest
import os
from pathlib import Path
from src.rag import GOSTRAGSystem
from src.config import config


# Маркер для интеграционных тестов
pytestmark = pytest.mark.skipif(
    not pytest.config.getoption("--integration", default=False),
    reason="Интеграционные тесты запускаются только с флагом --integration"
)


@pytest.fixture(scope="module")
def rag_system():
    """Фикстура RAG системы для интеграционных тестов"""
    # Проверка наличия API ключей
    if not config.openrouter.api_key or config.openrouter.api_key == "your_openrouter_api_key_here":
        pytest.skip("OPENROUTER_API_KEY не настроен")
    
    if not config.embedding.api_key or config.embedding.api_key == "your_openai_api_key_for_embeddings":
        pytest.skip("EMBEDDING_API_KEY не настроен")
    
    system = GOSTRAGSystem()
    yield system
    
    # Cleanup
    try:
        system.milvus_manager.disconnect()
    except:
        pass


@pytest.fixture(scope="module")
def test_document_path():
    """Путь к тестовому документу"""
    path = Path("/home/ubuntu/EvrazSosetHuiHAHAHAHAHA_CTO_VERSION_BITCHES/data/raw/GOST_27772-2021.pdf")
    if not path.exists():
        pytest.skip(f"Тестовый документ не найден: {path}")
    return str(path)


class TestFullIndexingCycle:
    """Тесты полного цикла индексирования"""
    
    def test_initialize_milvus(self, rag_system):
        """Тест инициализации Milvus"""
        rag_system.initialize_milvus(create_new=True)
        assert rag_system.milvus_manager is not None
    
    def test_load_documents(self, rag_system, test_document_path):
        """Тест загрузки документов"""
        documents = rag_system.load_documents(test_document_path)
        assert len(documents) > 0
        assert documents[0].text is not None
    
    def test_create_index(self, rag_system, test_document_path):
        """Тест создания индекса"""
        rag_system.initialize_milvus(create_new=True)
        documents = rag_system.load_documents(test_document_path)
        
        rag_system.create_index(documents, show_progress=False)
        
        # Проверка что индекс создан
        stats = rag_system.milvus_manager.get_collection_stats()
        assert stats is not None
        assert stats['num_entities'] > 0


class TestFullQueryCycle:
    """Тесты полного цикла запросов"""
    
    @pytest.fixture(autouse=True)
    def setup_index(self, rag_system, test_document_path):
        """Настройка индекса перед каждым тестом"""
        rag_system.initialize_milvus(create_new=True)
        documents = rag_system.load_documents(test_document_path)
        rag_system.create_index(documents, show_progress=False)
        rag_system.load_index()
        rag_system.setup_query_engine()
    
    def test_simple_query(self, rag_system):
        """Тест простого запроса"""
        result = rag_system.query("Что такое класс прочности?")
        
        assert result is not None
        assert 'answer' in result
        assert len(result['answer']) > 0
    
    def test_specific_class_query(self, rag_system):
        """Тест запроса о конкретном классе прочности"""
        result = rag_system.extract_strength_class_info("C235")
        
        assert result is not None
        assert 'class_name' in result
        assert result['class_name'] == "C235"
        assert 'properties' in result
    
    def test_multiple_queries(self, rag_system):
        """Тест множественных запросов"""
        queries = [
            "Что такое класс прочности C235?",
            "Какие механические свойства у стали?",
            "Перечисли классы прочности"
        ]
        
        for query in queries:
            result = rag_system.query(query)
            assert result is not None
            assert 'answer' in result


class TestErrorHandling:
    """Тесты обработки ошибок"""
    
    def test_query_without_index(self, rag_system):
        """Тест запроса без созданного индекса"""
        # Создаем новую систему без индекса
        new_system = GOSTRAGSystem()
        
        with pytest.raises(ValueError, match="Query engine"):
            new_system.query("test query")
    
    def test_load_nonexistent_document(self, rag_system):
        """Тест загрузки несуществующего документа"""
        with pytest.raises(Exception):
            rag_system.load_documents("/nonexistent/path/document.pdf")
    
    def test_empty_query(self, rag_system, test_document_path):
        """Тест пустого запроса"""
        rag_system.initialize_milvus(create_new=True)
        documents = rag_system.load_documents(test_document_path)
        rag_system.create_index(documents, show_progress=False)
        rag_system.load_index()
        rag_system.setup_query_engine()
        
        # Пустой запрос должен обрабатываться корректно
        result = rag_system.query("")
        assert result is not None


class TestPerformance:
    """Тесты производительности"""
    
    def test_indexing_time(self, rag_system, test_document_path, benchmark):
        """Тест времени индексирования"""
        def index_document():
            rag_system.initialize_milvus(create_new=True)
            documents = rag_system.load_documents(test_document_path)
            rag_system.create_index(documents, show_progress=False)
        
        # Benchmark требует pytest-benchmark
        if hasattr(pytest, 'benchmark'):
            benchmark(index_document)
    
    def test_query_time(self, rag_system, test_document_path):
        """Тест времени выполнения запроса"""
        import time
        
        rag_system.initialize_milvus(create_new=True)
        documents = rag_system.load_documents(test_document_path)
        rag_system.create_index(documents, show_progress=False)
        rag_system.load_index()
        rag_system.setup_query_engine()
        
        start = time.time()
        result = rag_system.query("Что такое класс прочности C235?")
        elapsed = time.time() - start
        
        # Запрос должен выполниться за разумное время (< 30 секунд)
        assert elapsed < 30
        assert result is not None


def pytest_addoption(parser):
    """Добавление опции --integration для pytest"""
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="Запустить интеграционные тесты"
    )


def pytest_configure(config):
    """Конфигурация pytest"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )

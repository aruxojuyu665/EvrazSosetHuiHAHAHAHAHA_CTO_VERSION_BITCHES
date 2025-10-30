"""
Тесты для локальных эмбеддингов
"""

import pytest
import os
import torch
from unittest.mock import patch, MagicMock


class TestLocalEmbeddings:
    """Тесты для локальных embedding моделей"""
    
    def test_cuda_availability(self):
        """Проверка доступности CUDA"""
        # Этот тест просто проверяет, что PyTorch установлен
        assert hasattr(torch, 'cuda')
        # Не требуем наличия GPU для прохождения теста
        cuda_available = torch.cuda.is_available()
        print(f"CUDA available: {cuda_available}")
        if cuda_available:
            print(f"CUDA device count: {torch.cuda.device_count()}")
            print(f"CUDA device name: {torch.cuda.get_device_name(0)}")
    
    @patch.dict(os.environ, {
        'EMBEDDING_TYPE': 'local',
        'LOCAL_EMBEDDING_MODEL': 'sentence-transformers/all-MiniLM-L6-v2',  # Легковесная модель для теста
        'LOCAL_EMBEDDING_DEVICE': 'cpu'
    })
    def test_local_embedding_config(self):
        """Тест конфигурации локальных эмбеддингов"""
        from src.config import config
        
        assert config.embedding.embedding_type == 'local'
        assert config.embedding.local_model == 'sentence-transformers/all-MiniLM-L6-v2'
        assert config.embedding.local_device == 'cpu'
    
    @patch.dict(os.environ, {
        'EMBEDDING_TYPE': 'openai',
        'EMBEDDING_MODEL': 'text-embedding-3-small',
        'EMBEDDING_API_KEY': 'test-key'
    })
    def test_openai_embedding_config(self):
        """Тест конфигурации OpenAI эмбеддингов"""
        from src.config import config
        
        assert config.embedding.embedding_type == 'openai'
        assert config.embedding.model == 'text-embedding-3-small'
        assert config.embedding.api_key == 'test-key'
    
    @pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available")
    def test_cuda_device_selection(self):
        """Тест выбора CUDA устройства"""
        device = torch.device('cuda:0')
        assert device.type == 'cuda'
        
        # Проверка, что можем создать тензор на GPU
        tensor = torch.zeros(1).to(device)
        assert tensor.is_cuda
    
    def test_cpu_device_selection(self):
        """Тест выбора CPU устройства"""
        device = torch.device('cpu')
        assert device.type == 'cpu'
        
        # Проверка, что можем создать тензор на CPU
        tensor = torch.zeros(1).to(device)
        assert not tensor.is_cuda
    
    @patch('src.rag.rag_system.HuggingFaceEmbedding')
    @patch.dict(os.environ, {
        'EMBEDDING_TYPE': 'local',
        'LOCAL_EMBEDDING_MODEL': 'intfloat/multilingual-e5-large',
        'LOCAL_EMBEDDING_DEVICE': 'cpu',
        'LOCAL_EMBEDDING_BATCH_SIZE': '16'
    })
    def test_rag_system_local_embeddings(self, mock_hf_embedding):
        """Тест инициализации RAG системы с локальными эмбеддингами"""
        from src.rag.rag_system import GOSTRAGSystem
        
        # Mock для HuggingFaceEmbedding
        mock_embed_instance = MagicMock()
        mock_hf_embedding.return_value = mock_embed_instance
        
        # Создание RAG системы
        rag = GOSTRAGSystem(openrouter_api_key='test-key')
        
        # Проверка, что HuggingFaceEmbedding был вызван с правильными параметрами
        mock_hf_embedding.assert_called_once()
        call_kwargs = mock_hf_embedding.call_args[1]
        
        assert call_kwargs['model_name'] == 'intfloat/multilingual-e5-large'
        assert call_kwargs['device'] == 'cpu'
        assert call_kwargs['embed_batch_size'] == 16
    
    @patch('src.rag.rag_system.OpenAIEmbedding')
    @patch.dict(os.environ, {
        'EMBEDDING_TYPE': 'openai',
        'EMBEDDING_MODEL': 'text-embedding-3-small',
        'EMBEDDING_API_KEY': 'test-openai-key'
    })
    def test_rag_system_openai_embeddings(self, mock_openai_embedding):
        """Тест инициализации RAG системы с OpenAI эмбеддингами"""
        from src.rag.rag_system import GOSTRAGSystem
        
        # Mock для OpenAIEmbedding
        mock_embed_instance = MagicMock()
        mock_openai_embedding.return_value = mock_embed_instance
        
        # Создание RAG системы
        rag = GOSTRAGSystem(
            openrouter_api_key='test-key',
            embedding_api_key='test-openai-key'
        )
        
        # Проверка, что OpenAIEmbedding был вызван
        mock_openai_embedding.assert_called_once()
        call_kwargs = mock_openai_embedding.call_args[1]
        
        assert call_kwargs['api_key'] == 'test-openai-key'
        assert call_kwargs['model'] == 'text-embedding-3-small'
    
    @patch.dict(os.environ, {
        'EMBEDDING_TYPE': 'invalid_type'
    })
    def test_invalid_embedding_type(self):
        """Тест обработки неверного типа эмбеддингов"""
        from src.rag.rag_system import GOSTRAGSystem
        
        with pytest.raises(ValueError, match="Неизвестный тип эмбеддингов"):
            rag = GOSTRAGSystem(openrouter_api_key='test-key')
    
    def test_batch_size_config(self):
        """Тест конфигурации размера батча"""
        with patch.dict(os.environ, {'LOCAL_EMBEDDING_BATCH_SIZE': '64'}):
            from src.config import config
            assert config.embedding.local_batch_size == 64
        
        with patch.dict(os.environ, {'LOCAL_EMBEDDING_BATCH_SIZE': 'invalid'}):
            from src.config import config
            # Должно вернуться значение по умолчанию
            assert config.embedding.local_batch_size == 32


@pytest.mark.integration
@pytest.mark.skipif(
    os.getenv('SKIP_INTEGRATION_TESTS', 'true').lower() == 'true',
    reason="Integration tests skipped"
)
class TestLocalEmbeddingsIntegration:
    """Интеграционные тесты для локальных эмбеддингов (требуют реальной модели)"""
    
    def test_load_small_model(self):
        """Тест загрузки легковесной модели"""
        from sentence_transformers import SentenceTransformer
        
        # Используем маленькую модель для быстрого теста
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        # Тест генерации эмбеддингов
        texts = ["Это тестовый текст", "Another test text"]
        embeddings = model.encode(texts)
        
        assert embeddings.shape[0] == 2
        assert embeddings.shape[1] == 384  # Размерность all-MiniLM-L6-v2
    
    @pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available")
    def test_model_on_gpu(self):
        """Тест работы модели на GPU"""
        from sentence_transformers import SentenceTransformer
        
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        model = model.to('cuda')
        
        texts = ["GPU test text"]
        embeddings = model.encode(texts)
        
        assert embeddings.shape[0] == 1
        assert embeddings.shape[1] == 384

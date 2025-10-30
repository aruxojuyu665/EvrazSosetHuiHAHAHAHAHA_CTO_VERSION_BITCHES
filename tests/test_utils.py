"""
Тесты для модуля утилит
"""

import pytest
import time
from unittest.mock import Mock, patch
from src.utils.retry_decorator import retry_on_error


def test_retry_success_first_attempt():
    """Тест успешного выполнения с первой попытки"""
    mock_func = Mock(return_value="success")
    decorated = retry_on_error(max_retries=3)(mock_func)
    
    result = decorated()
    
    assert result == "success"
    assert mock_func.call_count == 1


def test_retry_success_after_failures():
    """Тест успешного выполнения после нескольких неудач"""
    mock_func = Mock(side_effect=[Exception("fail"), Exception("fail"), "success"])
    decorated = retry_on_error(max_retries=3, delay=0.1)(mock_func)
    
    result = decorated()
    
    assert result == "success"
    assert mock_func.call_count == 3


def test_retry_all_attempts_fail():
    """Тест когда все попытки неудачны"""
    mock_func = Mock(side_effect=Exception("persistent error"))
    decorated = retry_on_error(max_retries=3, delay=0.1)(mock_func)
    
    with pytest.raises(Exception, match="persistent error"):
        decorated()
    
    assert mock_func.call_count == 3


def test_retry_exponential_backoff():
    """Тест экспоненциальной задержки между попытками"""
    mock_func = Mock(side_effect=[Exception("fail"), Exception("fail"), "success"])
    
    start_time = time.time()
    decorated = retry_on_error(max_retries=3, delay=0.1, backoff=2.0)(mock_func)
    result = decorated()
    elapsed = time.time() - start_time
    
    assert result == "success"
    # Первая задержка 0.1s, вторая 0.2s = минимум 0.3s
    assert elapsed >= 0.3


def test_retry_specific_exceptions():
    """Тест обработки только определенных исключений"""
    mock_func = Mock(side_effect=ValueError("value error"))
    decorated = retry_on_error(max_retries=3, delay=0.1, exceptions=(ValueError,))(mock_func)
    
    with pytest.raises(ValueError):
        decorated()
    
    assert mock_func.call_count == 3


def test_retry_unhandled_exception():
    """Тест что необработанные исключения пробрасываются сразу"""
    mock_func = Mock(side_effect=TypeError("type error"))
    decorated = retry_on_error(max_retries=3, delay=0.1, exceptions=(ValueError,))(mock_func)
    
    with pytest.raises(TypeError):
        decorated()
    
    # Должна быть только одна попытка, так как TypeError не в списке обрабатываемых
    assert mock_func.call_count == 1


def test_retry_with_arguments():
    """Тест что аргументы передаются корректно"""
    mock_func = Mock(return_value="success")
    decorated = retry_on_error(max_retries=3)(mock_func)
    
    result = decorated("arg1", "arg2", kwarg1="value1")
    
    assert result == "success"
    mock_func.assert_called_once_with("arg1", "arg2", kwarg1="value1")


def test_retry_preserves_function_metadata():
    """Тест что метаданные функции сохраняются"""
    @retry_on_error(max_retries=3)
    def sample_function():
        """Sample docstring"""
        return "result"
    
    assert sample_function.__name__ == "sample_function"
    assert sample_function.__doc__ == "Sample docstring"


def test_retry_logging(caplog):
    """Тест логирования попыток"""
    mock_func = Mock(side_effect=[Exception("fail"), "success"])
    decorated = retry_on_error(max_retries=3, delay=0.1)(mock_func)
    
    with caplog.at_level("WARNING"):
        result = decorated()
    
    assert result == "success"
    assert "Попытка 1/3 не удалась" in caplog.text


def test_retry_zero_delay():
    """Тест с нулевой задержкой"""
    mock_func = Mock(side_effect=[Exception("fail"), "success"])
    decorated = retry_on_error(max_retries=3, delay=0.0)(mock_func)
    
    start_time = time.time()
    result = decorated()
    elapsed = time.time() - start_time
    
    assert result == "success"
    # Должно выполниться практически мгновенно
    assert elapsed < 0.1

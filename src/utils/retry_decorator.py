"""
Декоратор для повторных попыток при ошибках API
"""

import time
import logging
from functools import wraps
from typing import Callable, Type, Tuple

logger = logging.getLogger(__name__)


def retry_on_error(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> Callable:
    """
    Декоратор для повторных попыток при ошибках
    
    Args:
        max_retries: Максимальное количество попыток
        delay: Начальная задержка между попытками (секунды)
        backoff: Множитель для увеличения задержки
        exceptions: Кортеж исключений для обработки
        
    Returns:
        Декорированная функция
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    func_name = getattr(func, '__name__', 'unknown_function')
                    
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"Попытка {attempt + 1}/{max_retries} не удалась для {func_name}: {e}. "
                            f"Повтор через {current_delay:.1f}с"
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(
                            f"Все {max_retries} попытки не удались для {func_name}: {e}"
                        )
            
            # Если все попытки не удались, выбрасываем последнее исключение
            raise last_exception
        
        return wrapper
    return decorator

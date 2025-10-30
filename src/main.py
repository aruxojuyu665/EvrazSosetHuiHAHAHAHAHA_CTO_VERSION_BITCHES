"""
Главный модуль для запуска системы анализа ГОСТ
"""

import argparse
import logging
from pathlib import Path


def setup_logging():
    """Настройка логирования"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def main():
    """Основная функция"""
    parser = argparse.ArgumentParser(
        description='ГОСТ Анализатор - извлечение данных из стандартов'
    )
    parser.add_argument(
        '--input',
        type=str,
        help='Путь к входному PDF файлу ГОСТ'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Путь к выходному файлу с результатами'
    )
    parser.add_argument(
        '--target',
        type=str,
        default='C235',
        help='Целевой объект для извлечения (например, класс прочности C235)'
    )
    
    args = parser.parse_args()
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Запуск ГОСТ Анализатора")
    logger.info(f"Целевой объект: {args.target}")
    
    # TODO: Реализовать логику обработки
    logger.warning("Функционал в разработке")


if __name__ == '__main__':
    main()

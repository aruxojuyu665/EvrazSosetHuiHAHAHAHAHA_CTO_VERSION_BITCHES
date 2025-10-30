"""
Главный модуль для запуска RAG системы анализа ГОСТ
"""

import argparse
import logging
import json
from pathlib import Path

from src.rag import GOSTRAGSystem
from src.config import config


def setup_logging(level: str = "INFO"):
    """Настройка логирования"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def index_documents(rag_system: GOSTRAGSystem, document_path: str, create_new: bool = False):
    """
    Индексирование документов
    
    Args:
        rag_system: RAG система
        document_path: Путь к документам
        create_new: Создать новый индекс
    """
    logger = logging.getLogger(__name__)
    
    logger.info(f"Индексирование документов из: {document_path}")
    
    # Инициализация Milvus
    rag_system.initialize_milvus(create_new=create_new)
    
    # Загрузка документов
    documents = rag_system.load_documents(document_path)
    
    # Создание индекса
    rag_system.create_index(documents, show_progress=True)
    
    logger.info("Индексирование завершено")


def query_system(rag_system: GOSTRAGSystem, question: str, output_file: str = None):
    """
    Выполнение запроса к системе
    
    Args:
        rag_system: RAG система
        question: Вопрос
        output_file: Файл для сохранения результата
    """
    logger = logging.getLogger(__name__)
    
    logger.info(f"Выполнение запроса: {question}")
    
    # Загрузка существующего индекса
    rag_system.initialize_milvus(create_new=False)
    rag_system.load_index()
    rag_system.setup_query_engine()
    
    # Выполнение запроса
    result = rag_system.query(question)
    
    # Вывод результата
    print("\n" + "="*80)
    print("ОТВЕТ:")
    print("="*80)
    print(result["answer"])
    print("\n" + "="*80)
    print("ИСТОЧНИКИ:")
    print("="*80)
    for i, source in enumerate(result["source_nodes"], 1):
        print(f"\n[{i}] Score: {source['score']:.4f}")
        print(f"Text: {source['text'][:200]}...")
    
    # Сохранение в файл если указан
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Результат сохранен в: {output_file}")


def extract_class_info(rag_system: GOSTRAGSystem, class_name: str, output_file: str = None):
    """
    Извлечение информации о классе прочности
    
    Args:
        rag_system: RAG система
        class_name: Название класса прочности
        output_file: Файл для сохранения результата
    """
    logger = logging.getLogger(__name__)
    
    logger.info(f"Извлечение информации о классе прочности: {class_name}")
    
    # Загрузка существующего индекса
    rag_system.initialize_milvus(create_new=False)
    rag_system.load_index()
    rag_system.setup_query_engine()
    
    # Извлечение информации
    result = rag_system.extract_strength_class_info(class_name)
    
    # Вывод результата
    print("\n" + "="*80)
    print(f"ИНФОРМАЦИЯ О КЛАССЕ ПРОЧНОСТИ {class_name}:")
    print("="*80)
    print(result["answer"])
    
    # Сохранение в файл
    if output_file:
        output_path = Path(output_file)
    else:
        output_path = config.paths.data_processed / f"{class_name}_info.json"
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Результат сохранен в: {output_path}")


def show_stats(rag_system: GOSTRAGSystem):
    """Показать статистику системы"""
    rag_system.initialize_milvus(create_new=False)
    stats = rag_system.get_stats()
    
    print("\n" + "="*80)
    print("СТАТИСТИКА СИСТЕМЫ:")
    print("="*80)
    print(json.dumps(stats, indent=2, ensure_ascii=False))


def main():
    """Основная функция"""
    parser = argparse.ArgumentParser(
        description='ГОСТ Анализатор - RAG система для извлечения данных из стандартов'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Команды')
    
    # Команда индексирования
    index_parser = subparsers.add_parser('index', help='Индексировать документы')
    index_parser.add_argument(
        '--input',
        type=str,
        required=True,
        help='Путь к документу или директории с документами'
    )
    index_parser.add_argument(
        '--create-new',
        action='store_true',
        help='Создать новый индекс (удалит существующий)'
    )
    
    # Команда запроса
    query_parser = subparsers.add_parser('query', help='Выполнить запрос')
    query_parser.add_argument(
        '--question',
        type=str,
        required=True,
        help='Вопрос для системы'
    )
    query_parser.add_argument(
        '--output',
        type=str,
        help='Файл для сохранения результата'
    )
    
    # Команда извлечения информации о классе прочности
    extract_parser = subparsers.add_parser('extract', help='Извлечь информацию о классе прочности')
    extract_parser.add_argument(
        '--class-name',
        type=str,
        default='C235',
        help='Название класса прочности (по умолчанию: C235)'
    )
    extract_parser.add_argument(
        '--output',
        type=str,
        help='Файл для сохранения результата'
    )
    
    # Команда статистики
    subparsers.add_parser('stats', help='Показать статистику системы')
    
    # Общие параметры
    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Уровень логирования'
    )
    
    args = parser.parse_args()
    
    # Настройка логирования
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    # Проверка конфигурации
    try:
        config.validate_config()
    except ValueError as e:
        logger.error(f"Ошибка конфигурации: {e}")
        logger.error("Убедитесь, что файл .env настроен правильно")
        return
    
    # Создание RAG системы
    rag_system = GOSTRAGSystem()
    
    # Выполнение команды
    if args.command == 'index':
        index_documents(rag_system, args.input, args.create_new)
    elif args.command == 'query':
        query_system(rag_system, args.question, args.output)
    elif args.command == 'extract':
        extract_class_info(rag_system, args.class_name, args.output)
    elif args.command == 'stats':
        show_stats(rag_system)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

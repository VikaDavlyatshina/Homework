import logging
from pathlib import Path

# Базовые пути
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT/ "data"
LOGS_DIR = PROJECT_ROOT/ "logs"
TEST_LOGS_DIR = LOGS_DIR/ "test"

# Создаем папку logs если её нет
LOGS_DIR.mkdir(exist_ok=True)
TEST_LOGS_DIR.mkdir(exist_ok=True)

# Пути к файлам с данными
JSON_FILE = DATA_DIR/ "operations.json"
CSV_FILE = DATA_DIR/ "transactions.csv"
EXCEL_FILE = DATA_DIR/ "transactions_excel.xlsx"

# Файлы логгов(перезаписываются при каждом запуске)
MASK_LOG_FILE = LOGS_DIR/ "masks.log"
UTILS_LOG_FILE = LOGS_DIR/ "utils.log"
FILE_READERS_LOG_FILE = LOGS_DIR/ "file_readers.log"

# Файлы логов для ТЕСТОВ (отдельные!)
TEST_MASKS_LOG_FILE = TEST_LOGS_DIR / "test_masks.log"
TEST_UTILS_LOG_FILE = TEST_LOGS_DIR / "test_utils.log"
TEST_FILE_READERS_LOG_FILE = TEST_LOGS_DIR / "test_file_readers.log"

# Формат логгов: метка времени, название модуля, уровень серьёзности, сообщение
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def setup_masks_logger():
    """Настройка логгера для модуля masks"""
    logger = logging.getLogger("masks")
    logger.setLevel(logging.DEBUG)

    # Обработчик для файла(mode='w' - перезаписывает при каждом запуске)
    # Создаем обработчик
    file_handler = logging.FileHandler(MASK_LOG_FILE, mode="w", encoding="utf-8")
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)

    # Очищаем старые обработчики и добавляем новый
    logger.handlers.clear()
    logger.addHandler(file_handler)

    return logger


def setup_utils_logger():
    """Настройка логгера для модуля utils"""
    logger = logging.getLogger("utils")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(UTILS_LOG_FILE, mode='w', encoding='utf-8')
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)

    logger.handlers.clear()
    logger.addHandler(file_handler)

    return logger


def setup_file_readers_logger():
    """Настройка логгера для основного приложения"""
    logger = logging.getLogger("file_readers")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(FILE_READERS_LOG_FILE, mode='w', encoding='utf-8')
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)

    logger.handlers.clear()
    logger.addHandler(file_handler)

    return logger


def setup_test_masks_logger():
    """Настройка логгера для ТЕСТОВ модуля masks"""
    logger = logging.getLogger("test_masks")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(TEST_MASKS_LOG_FILE, mode='w', encoding='utf-8')
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)

    logger.handlers.clear()
    logger.addHandler(file_handler)

    return logger


def setup_test_utils_logger():
    """Настройка логгера для ТЕСТОВ модуля utils"""
    logger = logging.getLogger("test_utils")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(TEST_UTILS_LOG_FILE, mode='w', encoding='utf-8')
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)

    logger.handlers.clear()
    logger.addHandler(file_handler)

    return logger


def setup_test_file_readers_logger():
    """Настройка логгера для основных ТЕСТОВ"""
    logger = logging.getLogger("test_main")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(TEST_FILE_READERS_LOG_FILE, mode='w', encoding='utf-8')
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)

    logger.handlers.clear()
    logger.addHandler(file_handler)

    return logger
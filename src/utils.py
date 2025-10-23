import json
from typing import Any, Dict, List, Union

from config import setup_utils_logger

logger = setup_utils_logger()


def read_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Функция загружает транзакции из JSON файла
    Args:
        file_path: Путь к JSON файлу
    Returns:
        list: Список словарей с данными о транзакциях или пустой список в случае ошибки
    """
    logger.debug(f"Начало чтения JSON файла: {file_path}")

    try:
        # Открываем файл
        with open(file_path, "r", encoding="utf-8") as file:
            data: Union[List[Dict[str, Any]], Dict[str, Any]] = json.load(file)

        logger.debug(f"Файл успешно прочитан, получено данных: {len(data) if isinstance(data, list) else 'не список'}")

        # Проверяем, что данные являются списком
        if not isinstance(data, list):
            logger.warning(f"Данные JSON не являются списком, тип: {type(data)}")
            return []

        logger.info(f"Успешно загружено {len(data)} транзакций из файла {file_path}")
        return data

    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования  JSON в файле {file_path}: {e}")
        return []

    except Exception as e:
        logger.error(f"Неизвестная ошибка при чтении {file_path}: {e}")
        return []

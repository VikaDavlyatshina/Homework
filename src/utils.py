import json
import logging
import os
from typing import Any, Dict, List

# Создаем папку logs если она не существует
if not os.path.exists("logs"):
    os.makedirs("logs")

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)

# Создаем обработчик
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

# добавляем обработчик, чтобы избежать дублирования
if not logger.hasHandlers():
    logger.addHandler(file_handler)


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Функция загружает транзакции из JSON файла
    Args:
        file_path: Путь к JSON файлу
    Returns:
        list: Список словарей с данными о транзакциях или пустой список в случае ошибки
    """

    # Проверяем существования файла
    if not os.path.isfile(file_path):
        logger.warning(f"Файл не найден: {file_path}")
        return []

    try:
        # Открываем файл и загружаем данные
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.info(f"Файл успешно загружен: {file_path}")

        # Проверяем, что данные являются списком
        if not isinstance(data, list):
            logger.warning(f"Некорректный формат данных в файле {file_path}: ожидается список, получен {type(data)}")
            return []

        logger.info(f"Из файла {file_path} загружено {len(data)} транзакций")
        return data

    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле: {file_path}")
        return []
    except Exception as e:
        logger.exception(f"Неожиданная ошибка при чтении файла {file_path}: {e}")
        return []

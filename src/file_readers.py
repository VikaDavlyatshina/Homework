import logging
import os
from typing import Any, Dict, List, cast

import pandas as pd

# Создаем папку logs если она не существует
if not os.path.exists("logs"):
    os.makedirs("logs")

logger = logging.getLogger("file_readers")
logger.setLevel(logging.INFO)

# Создаем обработчик
file_handler = logging.FileHandler("logs/file_readers.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

# добавляем обработчик, чтобы избежать дублирования
if not logger.hasHandlers():
    logger.addHandler(file_handler)


def read_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла
    Args:
       file_path(str): путь к CSV-файлу
    Returns:
        List[Dict[str, Any]]: Список транзакций в виде словарей
    """
    logger.info(f"Начало чтения CSV-файла: {file_path}")

    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        # Открываем файл
        df = pd.read_csv(file_path, encoding="utf-8")
        transactions = cast(List[Dict[str, Any]], df.to_dict(orient="records"))

        logger.info(f"Успешно прочитано {len(transactions)} транзакций в CSV-файле")
        return transactions

    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Ошибка при чтении CSV-файла {file_path}: {e}")
        raise ValueError(f"Неверный формат CSV-файла '{file_path}': {e}")


def read_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из Excel-файла
    Args:
       file_path(str): путь к Excel-файлу
    Returns:
        List[Dict[str, Any]]: Список транзакций в виде словарей
    """
    logger.info(f"Начало чтения Excel-файла: {file_path}")

    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        # Открываем файл
        df = pd.read_excel(file_path)
        transactions = cast(List[Dict[str, Any]], df.to_dict(orient="records"))

        logger.info(f"Успешно прочитано {len(transactions)} транзакций в Excel-файле")
        return transactions
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Ошибка при чтении Excel-файла {file_path}: {e}")
        raise ValueError(f"Неверный формат Excel-файла: {e}")

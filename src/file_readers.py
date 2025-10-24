from pathlib import Path
from typing import Any, Dict, List, cast

import pandas as pd

from config import setup_file_readers_logger

# Создаем логгер
logger = setup_file_readers_logger()


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
        if not Path(file_path).exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        # Открываем файл
        df = pd.read_csv(file_path, encoding="utf-8", sep=";")
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
        if not Path(file_path).exists():
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

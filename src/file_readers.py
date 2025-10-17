from typing import List, Dict, Any
import pandas as pd
import os
import logging

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


def read_transactions_from_csv(file_path: str) ->List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла
    Args:
       file_path(str): путь к CSV-файлу
    Returns:
        List[Dict[str, str]]: Список транзакций в виде словарей
    """
    logger.info(f"Начало чтения CSV-файла: {file_path}")

    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError("Файл не найден: {file_path}")

        df = pd.read_csv(file_path)
        transactions =  df.to_dict(orient='records')

        logger.info(f"Успешно прочитано {len(transactions)} транзакций в CSV-файле")
        return transactions

    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Ошибка при чтении CSV-файла {file_path}: {e}")
        raise ValueError(f"Неверный формат CSV-файла: {e}")

def read_transactions_from_excel(file_path: str) ->List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла
    Args:
       file_path(str): путь к Excel-файлу
    Returns:
        List[Dict[str, str]]: Список транзакций в виде словарей
    """
    df = pd.read_excel(file_path)
    transactions =  df.to_dict(orient='records')
    return transactions


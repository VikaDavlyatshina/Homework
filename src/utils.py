import json
import os
from typing import List, Dict, Any


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Функция загружает транзакции из JSON файла
    Args:
        file_path: Путь к JSON файлу
    Returns:
        list: Список словарей с данными о транзакциях или пустой список в случае ошибки
    """
    try:
        # Проверяем существования файла
        if not os.path.isfile(file_path):
            return []

        # Открываем файл
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем, что данные являются списком
        if not isinstance(data, list):
            return []

        return data

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        return []





















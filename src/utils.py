import json
import os
from typing import List, Dict, Any


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """ Функция принимает на вход путь до JSON-файла и возвращает список словарей о финансовых транзакциях
    Args:
         file_path(str): Принимает путь до файла с транзакциями
    Return:
        List[Dict[str, Any]]: Возвращает список словарей с данными о транзакциях"""

    # Получение пути к файлу
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    correct_file_path = os.path.join(project_root, "data", "operations.json")


    # Проверка существования файла
    if not os.path.isfile(correct_file_path):
        return []

    try:
        with open(correct_file_path, 'r', encoding='utf-8') as file:
            # Читаем и проверяем, что файл не пустой
            content = file.read().strip()
            if not content:
                return []

        # Извлекаем данные
        data = json.loads(content)

        # Проверяем, что данные являются списком
        if isinstance(data, list):
            return data
        else:
            return[]
        # Ловим ошибки
    except (json.JSONDecodeError, Exception):
        return []




























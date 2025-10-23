import re
from typing import Dict, List


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """Ищет транзакции по строке описания используя регулярные выражения"""
    # Проверяем, что данные не пустые
    if not data and search:
        return []

    found_operations = []

    # Перебираем каждую операцию в списке
    for operation in data:
        # Получаем описание операции
        description = operation.get("description", "")

        # Используем регулярное выражение для поиска
        # re.escape Экранирует специальные символы, чтобы искались как обычный текст
        # re.IGNORECASE - поиск без учета регистра
        pattern = re.escape(search)
        if re.search(pattern, description, re.IGNORECASE):
            found_operations.append(operation)

    return found_operations


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Считает количество операций по категориям
    """
    # Проверяем, что данные не пустые
    if not data:
        return {category: 0 for category in categories}

    # Создаём словарь для результатов, заполняем нулями
    result = {}
    for category in categories:
        result[category] = 0

    # Перебираем все операции
    for operation in data:
        description = operation.get("description", "").lower()

        # Проверяем каждую категорию
        for category in categories:
            # Ищем категорию в описании (без учета регистра)
            if category.lower() in description:
                result[category] += 1

    return result

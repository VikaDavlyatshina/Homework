import re
from collections import defaultdict
from typing import List, Dict
from src.utils import read_transactions_from_json


def process_bank_search(data: List[Dict], search: str)->List[Dict]:
    """Функция фильтрации списка операций по наличию строки в описании.

    Args:
        data: Список словарей с данными о банковских операциях
        search: Строка для поиска в описании

    Returns: Отфильтрованный список операций
     """
    # Создаём регулярное выражение, которое ищет строку вне зависимости от регистра.
    # Используем re.escape, чтобы в поисковой строке не возникли ошибки со спецсимволами.
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    # Создаём список для результата
    result = []

    # Перебираем все операции
    for operation in data:
        description = operation.get('description', '') # получаем описание или пустую строку
        # Ищем совпадение по шаблону
        if pattern.search(description):
            result.append(operation)
    return result

def process_bank_operations(data:List[Dict], categories:List[str])-> Dict[str, int]:

    # Создаём словарь для подсчета
    counts = defaultdict(int)

    for operation in data:
        description = operation.get('description', '').lower() # делаем описание строчным, чтобы было проще искать
        for category in categories:
            # Проверяем наличие категории в описании
            if category.lower() in description:
                counts[category] += 1

    # Преобразуем в словарь
    return dict(counts)

if __name__ == '__main__':
    data = read_transactions_from_json('data/operations.json')
    search_term = "со счета на"
    search_results = process_bank_search(data, search_term)

    print("Результаты поиска по слову '{}':".format(search_term))
    for item in search_results:
        print(item)

    categories = ["Счет"]
    counts = process_bank_operations(data, categories)

    print("Подсчет по категориям:")
    for category, count in counts.items():
        print(f"{category}: {count}")
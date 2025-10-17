import json
from typing import List, Dict, Any
import logging
import os

# Создаем папку logs если она не существует
if not os.path.exists('logs'):
    os.makedirs('logs')

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('logs/utils.log', mode='w', encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
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


# Для тестирования прямо из этого файла
if __name__ == "__main__":
    # Создайте тестовые файлы для проверки

    # 1. правильный JSON список
    with open("test_valid.json", "w", encoding='utf-8') as f:
        json.dump([{"id": 1, "amount": 100}, {"id": 2, "amount": 200}], f)

    # 2. некорректный JSON
    with open("test_invalid.json", "w", encoding='utf-8') as f:
        f.write("{ invalid json }")

    # 3. JSON не список
    with open("test_not_list.json", "w", encoding='utf-8') as f:
        json.dump({"key": "value"}, f)

    # 4. Не существующий файл
    nonexistent_path = "nonexistent_file.json"

    print("Тест с правильным JSON:")
    print(read_json_file("test_valid.json"))

    print("\nТест с некорректным JSON:")
    print(read_json_file("test_invalid.json"))

    print("\nТест с JSON, не являющимся списком:")
    print(read_json_file("test_not_list.json"))

    print("\nТест с несуществующим файлом:")
    print(read_json_file(nonexistent_path))
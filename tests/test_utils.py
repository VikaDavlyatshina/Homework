import json
import os
import unittest
from typing import ClassVar

from src.utils import read_transactions_from_json


class TestReadJsonFile(unittest.TestCase):
    """Набор тестов для проверки функции read_json_file"""

    test_dir: ClassVar[str] = ""

    @classmethod
    def setUpClass(cls) -> None:
        # Создаём временный файлы и ресурсы для тестов
        cls.test_dir = "tests/test_dir"  # Путь для временных файлов
        os.makedirs(cls.test_dir, exist_ok=True)  # Создаём директорию, если не существует

        # Создаём валидный JSON-файл со списком словарей
        with open(os.path.join(cls.test_dir, "valid.json"), "w", encoding="utf-8") as f:
            json.dump(
                [
                    {"id": 441945886, "state": "EXECUTED", "date": "2019-08-26T10:50:58.294041"},
                    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                ],
                f,
            )

        # Создаём файл с данными, которые не являются списком
        with open(os.path.join(cls.test_dir, "not_list.json"), "w", encoding="utf-8") as f:
            json.dump({"id": 441945886, "state": "EXECUTED", "date": "2019-08-26T10:50:58.294041"}, f)

        # Создаём пустой файл
        with open(os.path.join(cls.test_dir, "empty.json"), "w", encoding="utf-8") as f:
            f.write("")

        # Создаём файл с некорректными данными
        with open(os.path.join(cls.test_dir, "invalid_json.json"), "w", encoding="utf-8") as f:
            f.write("{this is not: valid json}")

    @classmethod
    def tearDownClass(cls) -> None:
        # Удаляем созданные данные и папку после тестов

        for file in os.listdir(cls.test_dir):
            os.remove(os.path.join(cls.test_dir, file))
        os.rmdir(cls.test_dir)

    def test_valid_file(self) -> None:
        # Тестируем чтение корректного файла -> должен возвращать список словарей

        path = os.path.join(self.test_dir, "valid.json")
        result = read_transactions_from_json(path)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertTrue(all(isinstance(item, dict) for item in result))

    def test_file_empty(self) -> None:
        # Тестирование, когда файл пустой
        path = os.path.join(self.test_dir, "empty.json")
        result = read_transactions_from_json(path)
        self.assertEqual(result, [])

    def test_file_invalid_json(self) -> None:
        # Тестирование файла с некорректными данными
        path = os.path.join(self.test_dir, "invalid_json.json")
        result = read_transactions_from_json(path)
        self.assertEqual(result, [])

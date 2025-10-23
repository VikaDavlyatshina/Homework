import json

from src.utils import read_transactions_from_json


class TestReadTransactionsFromJSON:
    """Тесты для функции read_transactions_from_json"""

    def test_valid_json_file(self, tmp_path):
        """Тест корректного JSON файла"""
        # Создаем временный файл
        test_file = tmp_path / "test.json"
        test_data = [{"id": 1, "amount": 100, "description": "Test transaction"}]

        test_file.write_text(json.dumps(test_data), encoding="utf-8")

        result = read_transactions_from_json(str(test_file))

        assert len(result) == 1
        assert result[0]["id"] == 1
        assert result[0]["description"] == "Test transaction"

    def test_file_not_found(self):
        """Тест когда файл не существует"""
        result = read_transactions_from_json("nonexistent_file.json")
        assert result == []

    def test_invalid_json(self, tmp_path):
        """Тест некорректного JSON"""
        test_file = tmp_path / "bad.json"
        test_file.write_text("{ invalid json }", encoding="utf-8")

        result = read_transactions_from_json(str(test_file))
        assert result == []

    def test_json_dict_instead_of_list(self, tmp_path):
        """Тест когда JSON содержит словарь вместо списка"""
        test_file = tmp_path / "dict.json"
        test_file.write_text(json.dumps({"key": "value"}), encoding="utf-8")

        result = read_transactions_from_json(str(test_file))
        assert result == []

    def test_empty_file(self, tmp_path):
        """Тест пустого файла"""
        test_file = tmp_path / "empty.json"
        test_file.write_text("", encoding="utf-8")

        result = read_transactions_from_json(str(test_file))
        assert result == []

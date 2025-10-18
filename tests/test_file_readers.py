import os
import tempfile
from typing import Any, Dict, List

import pandas as pd
import pytest

from src.file_readers import read_transactions_from_csv, read_transactions_from_excel


class TestTransactionsSimple:
    """Простые тесты с фикстурой данных"""

    def test_sample_operations_fixture(self, transactions: List[Dict[str, Any]]) -> None:
        """Тест правильной работы фикстуры с данными"""

        assert len(transactions) == 5
        assert transactions[0]["id"] == 939719570
        assert transactions[4]["state"] == "CANCELED"

    def test_read_transactions_from_csv(self, transactions: List[Dict[str, Any]]) -> None:
        """Тестируем чтение CSV с созданием файла в тесте"""

        # Создаём временный файл
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
            df = pd.DataFrame(transactions)  # Преобразуем тестовые данные в таблицу (DataFrame)
            df.to_csv(f.name, index=False, encoding="utf-8")  # Преобразуем таблицу в CSV-файл
            csv_file = f.name  # Сохраняем путь к файлу

        try:
            result = read_transactions_from_csv(csv_file)

            assert len(result) == len(transactions)
            assert result[0]["id"] == 939719570
            assert result[0]["description"] == "Перевод организации"
            assert result[3]["description"] == "Перевод с карты на карту"

        finally:
            # Удаляем временный файл
            if os.path.exists(csv_file):  # Проверяем существование файла
                os.unlink(csv_file)  # Удаляем

    def test_read_transactions_from_excel(self, transactions: List[Dict[str, Any]]) -> None:
        """Тестируем чтение Excel с созданием файла в тесте"""

        # Создаём временный файл
        with tempfile.NamedTemporaryFile(mode="w", suffix=".xlsx", delete=False) as f:
            df = pd.DataFrame(transactions)  # Преобразуем тестовые данные в таблицу (DataFrame)
            df.to_excel(f.name, index=False)  # Преобразуем таблицу в CSV-файл
            xlsx_file = f.name  # Сохраняем путь к файлу

        try:
            result = read_transactions_from_excel(xlsx_file)

            assert len(result) == len(transactions)

            executed_trans = [tran for tran in result if tran["state"] == "EXECUTED"]
            canceled_trans = [tran for tran in result if tran["state"] == "CANCELED"]

            assert len(executed_trans) == 4
            assert len(canceled_trans) == 1

        finally:
            # Удаляем временный файл
            if os.path.exists(xlsx_file):  # Проверяем существование файла
                os.unlink(xlsx_file)  # Удаляем


class TestTransactionsErrors:
    """Тесты обработки ошибок"""

    def test_csv_file_not_found(self) -> None:
        """Тестируем обработку отсутствия CSV-файла"""

        with pytest.raises(FileNotFoundError):
            read_transactions_from_csv("Файл не найден")

    def test_csv_invalid_file(self, transactions: List[Dict[str, Any]]) -> None:
        """Тестируем обработку некорректного CSV-файла"""

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".csv", delete=False) as f:
            # Создаем пустой файл
            invalid_file = f.name

        try:
            with pytest.raises(ValueError, match="Неверный формат CSV-файла"):
                read_transactions_from_csv(invalid_file)

        finally:
            os.unlink(invalid_file)  # Удаляем

    def test_excel_file_not_found(self) -> None:
        """Тестируем обработку отсутствия Excel-файла"""

        with pytest.raises(FileNotFoundError):
            read_transactions_from_excel("Файл не найден")

    def test_excel_invalid_file(self, transactions: List[Dict[str, Any]]) -> None:
        """Тестируем обработку некорректного Excel-файла"""

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".xlsx", delete=False) as f:
            # Создаем пустой файл
            invalid_file = f.name

        try:
            with pytest.raises(ValueError, match="Неверный формат Excel-файла"):
                read_transactions_from_excel(invalid_file)

        finally:
            os.unlink(invalid_file)  # Удаляем


class TestTransactionsParametrized:
    """Параметризованные тесты"""

    @pytest.mark.parametrize(
        "transaction_index,expected_id,expected_description",
        [
            (0, 939719570, "Перевод организации"),
            (1, 142264268, "Перевод со счета на счет"),
            (2, 873106923, "Перевод со счета на счет"),
            (3, 895315941, "Перевод с карты на карту"),
            (4, 594226727, "Перевод организации"),
        ],
    )
    def test_specific_transaction(
        self, transactions: List[Dict[str, Any]], transaction_index: int, expected_id: int, expected_description: str
    ) -> None:
        """Параметризованный тест конкретных операций"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
            df = pd.DataFrame(transactions)
            df.to_csv(f.name, index=False, encoding="utf-8")
            csv_file = f.name

        try:
            transactions = read_transactions_from_csv(csv_file)

            assert transactions[transaction_index]["id"] == expected_id
            assert transactions[transaction_index]["description"] == expected_description

        finally:
            if os.path.exists(csv_file):
                os.unlink(csv_file)

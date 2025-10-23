from unittest.mock import Mock, patch

import pytest

from src.file_readers import read_transactions_from_csv, read_transactions_from_excel


class TestFileReaders:
    """Тесты для функций чтения CSV и Excel файлов"""

    # Тестовые данные - то, что должны вернуть наши функции
    SAMPLE_TRANSACTIONS = [
        {
            "id": 1,
            "date": "2024-01-15",
            "amount": 100,
            "currency": "USD",
            "description": "Payment",
            "from": "1234567890123456",
            "to": "9876543210987654",
        },
        {
            "id": 2,
            "date": "2024-01-16",
            "amount": 200,
            "currency": "RUB",
            "description": "Transfer",
            "from": "1111222233334444",
            "to": "5555666677778888",
        },
    ]

    def test_read_transactions_from_csv_success(self):
        """
        Тест 1: Успешное чтение CSV файла
        Проверяем, что функция правильно читает CSV и возвращает список словарей
        """
        # Создаем "заглушку" для проверки существования файла
        with patch("src.file_readers.Path.exists") as mock_exists:
            # Говорим заглушке всегда возвращать True (файл существует)
            mock_exists.return_value = True

            # Создаем заглушку для pandas.read_csv
            with patch("pandas.read_csv") as mock_read_csv:
                # Создаем fake DataFrame (имитация таблицы pandas)
                fake_dataframe = Mock()
                # Говорим fake DataFrame возвращать наши тестовые данные
                fake_dataframe.to_dict.return_value = self.SAMPLE_TRANSACTIONS
                # Подставляем fake DataFrame вместо реального
                mock_read_csv.return_value = fake_dataframe

                # ВЫЗОВ ФУНКЦИИ: пробуем прочитать CSV
                result = read_transactions_from_csv("test.csv")

                # ПРОВЕРКИ:
                # 1. Проверяем что функция вернула правильные данные
                assert result == self.SAMPLE_TRANSACTIONS

                # 2. Проверяем что проверили существование файла
                mock_exists.assert_called_once()

                # 3. Проверяем что вызвали read_csv с правильными параметрами
                mock_read_csv.assert_called_once_with("test.csv", encoding="utf-8", sep=";")

    def test_read_transactions_from_csv_file_not_found(self):
        """
        Тест 2: Файл не найден
        Проверяем, что функция выдает ошибку когда файла нет
        """
        with patch("src.file_readers.Path.exists") as mock_exists:
            # Говорим заглушке возвращать False (файл не существует)
            mock_exists.return_value = False

            # ПРОВЕРКА: ожидаем, что функция выбросит FileNotFoundError
            with pytest.raises(FileNotFoundError) as error_info:
                read_transactions_from_csv("missing_file.csv")

            # Проверяем текст ошибки
            assert "Файл не найден: missing_file.csv" in str(error_info.value)

    def test_read_transactions_from_csv_bad_format(self):
        """
        Тест 3: Неправильный формат CSV
        Проверяем обработку ошибок при чтении битого файла
        """
        with patch("src.file_readers.Path.exists") as mock_exists:
            mock_exists.return_value = True

            with patch("pandas.read_csv") as mock_read_csv:
                # Имитируем ошибку при чтении CSV
                mock_read_csv.side_effect = Exception("File is corrupted")

                # ПРОВЕРКА: ожидаем ValueError с правильным сообщением
                with pytest.raises(ValueError) as error_info:
                    read_transactions_from_csv("corrupted.csv")

                # Проверяем что в ошибке есть информация о файле
                assert "Неверный формат CSV-файла 'corrupted.csv'" in str(error_info.value)

    def test_read_transactions_from_excel_success(self):
        """
        Тест 4: Успешное чтение Excel файла
        Проверяем чтение Excel файлов
        """
        with patch("src.file_readers.Path.exists") as mock_exists:
            mock_exists.return_value = True

            with patch("pandas.read_excel") as mock_read_excel:
                # Создаем fake DataFrame для Excel
                fake_dataframe = Mock()
                fake_dataframe.to_dict.return_value = self.SAMPLE_TRANSACTIONS
                mock_read_excel.return_value = fake_dataframe

                # ВЫЗОВ ФУНКЦИИ
                result = read_transactions_from_excel("test.xlsx")

                # ПРОВЕРКИ
                assert result == self.SAMPLE_TRANSACTIONS
                mock_exists.assert_called_once()
                # Для Excel не указываем encoding и sep
                mock_read_excel.assert_called_once_with("test.xlsx")

    def test_read_transactions_from_excel_file_not_found(self):
        """
        Тест 5: Excel файл не найден
        """
        with patch("src.file_readers.Path.exists") as mock_exists:
            mock_exists.return_value = False

            with pytest.raises(FileNotFoundError) as error_info:
                read_transactions_from_excel("missing_excel.xlsx")

            assert "Файл не найден: missing_excel.xlsx" in str(error_info.value)

    def test_read_transactions_from_excel_bad_format(self):
        """
        Тест 6: Неправильный формат Excel
        """
        with patch("src.file_readers.Path.exists") as mock_exists:
            mock_exists.return_value = True

            with patch("pandas.read_excel") as mock_read_excel:
                # Имитируем ошибку чтения Excel
                mock_read_excel.side_effect = Exception("Not an Excel file")

                with pytest.raises(ValueError) as error_info:
                    read_transactions_from_excel("not_excel.xlsx")

                assert "Неверный формат Excel-файла" in str(error_info.value)

    def test_read_empty_csv_file(self):
        """
        Тест 7: Чтение пустого CSV файла
        Проверяем что функция работает с пустыми файлами
        """
        with patch("src.file_readers.Path.exists") as mock_exists:
            mock_exists.return_value = True

            with patch("pandas.read_csv") as mock_read_csv:
                # Создаем fake DataFrame с пустым списком
                fake_dataframe = Mock()
                fake_dataframe.to_dict.return_value = []  # Пустой список
                mock_read_csv.return_value = fake_dataframe

                result = read_transactions_from_csv("empty.csv")

                # Проверяем что вернулся пустой список
                assert result == []
                assert len(result) == 0

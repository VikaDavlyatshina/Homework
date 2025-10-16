import unittest
from unittest.mock import patch, Mock
from typing import Any, Dict, Optional
from src.external_api import converting_a_transactions_into_rub


class TestConvertTransactionsToRub(unittest.TestCase):
    """Набор тестов для проверки функции converting_a_transactions_into_rub"""

    # Проверяем случай, когда транзакция в рублях
    @patch("src.external_api.requests.get")
    def test_rub_currency(self, mock_get: Mock) -> None:
        # Входящая транзакция с валютой "RUB"
        transaction: Dict[str, Any] = {
            "operationAmount": {"amount": "1000", "currency": {"name": "руб.", "code": "RUB"}}
        }
        # Вызов функции и проверка результатов
        result: Optional[float] = converting_a_transactions_into_rub(transaction)
        self.assertEqual(result, 1000)

    # Тест успешной проверки "USD" в "RUB"
    @patch("src.external_api.requests.get")
    def test_usd_conversion_success(self, mock_get: Mock) -> None:
        # Создаём имитацию API ключа с курсом
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 80500}
        mock_get.return_value = mock_response

        # Входящая транзакция
        transaction: Dict[str, Any] = {
            "operationAmount": {"amount": "1000", "currency": {"name": "USD", "code": "USD"}}
        }
        # Вызов функции и проверка результата.
        result: Optional[float] = converting_a_transactions_into_rub(transaction)
        self.assertEqual(result, 80500)
        mock_get.assert_called_once()

    # Тест успешной конвертации EUR
    @patch("src.external_api.requests.get")
    def test_eur_conversion_success(self, mock_get: Mock) -> None:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 112932}
        mock_get.return_value = mock_response

        # Пример транзакции
        transaction: Dict[str, Any] = {
            "operationAmount": {"amount": "1200", "currency": {"name": "EUR", "code": "EUR"}}
        }
        # Вызываем функцию и проверяем результат
        result: Optional[float] = converting_a_transactions_into_rub(transaction)
        self.assertEqual(result, 112932)

    def test_missing_operationAmount(self) -> None:
        transactions: Dict[str, Any] = {"Code": "zlt"}
        result = converting_a_transactions_into_rub(transactions)
        self.assertIsNone(result)

    @patch("src.external_api.requests.get")
    def test_api_error_response(self, mock_get: Mock) -> None:

        # Тест обработки ошибки API (статус 500).

        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response

        # Входящая транзакция в USD
        transaction: Dict[str, Any] = {
            "operationAmount": {"amount": "1000", "currency": {"name": "USD", "code": "USD"}}
        }
        # Вызов функции
        result = converting_a_transactions_into_rub(transaction)
        # Проверка, что возвращается None при ошибке
        self.assertIsNone(result)

    def test_unsupported_currency(self) -> None:
        transactions: Dict[str, Any] = {
            "operationAmount": {"amount": "1500", "currency": {"name": "EGP", "code": "EGP"}}
        }

        result = converting_a_transactions_into_rub(transactions)
        self.assertIsNone(result)

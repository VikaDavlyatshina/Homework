from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator:
    """Функция, которая принимает на вход список транзакций и поочередно выдает транзакции,
    соответствующие заданной валюте"""
    for transaction in transactions:
        try:
            if transaction.get("currency_code") == currency_code:
                yield transaction
            elif transaction.get("operationAmount", {}).get("currency", {}).get("code", {}) == currency_code:
                yield transaction
        except (AttributeError, TypeError):
            # Если структура данных некорректна, пропускаем транзакцию
            continue


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator:
    """Генератор, который принимает список словарей с транзакциями
    и возвращает описание каждой операции по очереди"""
    for transaction in transactions:
        yield transaction.get("description", "Нет описания")


def card_number_generator(start: int, end: int) -> Iterator:
    """Генератор, который выдает номера банковских карт в формате 0000 0000 0000 0000,
    где 0 — цифра номера карты"""
    if start < 1:
        start = 1
    for number in range(start, end + 1):
        # Преобразуем число в строку с ведущими нулями с помощью метода zfill()
        number_str = str(number).zfill(16)

        # Разделяем строку на части по 4 символа
        parts = [number_str[i : i + 4] for i in range(0, 16, 4)]

        # Объединяем части с пробелами
        yield " ".join(parts)

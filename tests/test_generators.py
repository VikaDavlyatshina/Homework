import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

 #Тестирование генераторной функции filter_by_currency

def test_filter_by_currency_usd(transactions):
    # Тестирование фильтрации по валюте USD
    filtered = list(filter_by_currency(transactions,"USD"))
    for trans in filtered:
        assert trans["operationAmount"]["currency"]["code"] == "USD"
    assert len(filtered) == 3


def test_filter_by_currency_rub(transactions):
    # Тестирование фильтрации по валюте RUB
    filtered = list(filter_by_currency(transactions,"RUB"))
    for trans in filtered:
        assert trans["operationAmount"]["currency"]["code"] == "RUB"
    assert len(filtered) == 2

def test_filter_by_currency_empty_transactions():
    # Тестирование при отсутствии списка транзакций
    result = list(filter_by_currency([], "USD"))
    assert result == []


def test_filter_by_currency_no_matches(transactions):
    # Тестирование при отсутствии заданной валюты
     result = list(filter_by_currency(transactions, "EUR"))
     assert result == []

def test_filter_by_currency_empty():
    # Тестирование обработки пустого списка
    result = list(filter_by_currency([], []))
    assert result == []

# Тестирование генератора transaction_descriptions
def test_transaction_descriptions(transactions):
    gen = list(transaction_descriptions(transactions))
    assert gen == ["Перевод организации",
                   "Перевод со счета на счет",
                   "Перевод со счета на счет",
                   "Перевод с карты на карту",
                   "Перевод организации"]


def test_transaction_descriptions_sample(sample_description):
    gen = list(transaction_descriptions(sample_description))
    assert gen == ["Перевод организации",
                   "Нет описания",
                   "Перевод со счета на счет",
                   "Нет описания",
                   "Перевод организации"]

@pytest.mark.parametrize(
    "data, expected",
    [
        (
            [{"description": "Оплата услуги"}, {"from": "Счет 123"}],
            ["Оплата услуги", "Нет описания"],
        ),
        (
            [{"description": "Перевод с карты на карту"}, {"description": "Перевод со счета на счет"}, {"description": 123}],
            ["Перевод с карты на карту", "Перевод со счета на счет", 123],
        ),
        (
            [{"description": "---"}, {"description": "Перевод организации"}],
            ["---", "Перевод организации"],
        ),
        ( [],
          [],),
    ],
)
def test_transaction_descriptions_simple(data, expected):
    result = list(transaction_descriptions(data))
    assert result == expected

# Тестирование генератора card_number_generator

@pytest.mark.parametrize("start, end, expected",
                         [
                             # Одна карта
                             (1,1,["0000 0000 0000 0001"]),
                             # Несколько карт
                             (1, 3, ["0000 0000 0000 0001",
                                     "0000 0000 0000 0002",
                                     "0000 0000 0000 0003"]),
                             # Минимальное значение
                             (0, 1, ["0000 0000 0000 0001"]),
                             # Отработка нулевого значения
                             (0, 0, []),

                             # Если start > end
                             (5, 4, []),
                             # Максимальное значение
                             (9999999999999998, 9999999999999999,
                                    ["9999 9999 9999 9998",
                                     "9999 9999 9999 9999"])

                         ])
def test_card_number_generator(start,end, expected):
    result = list(card_number_generator(start, end))
    assert result == expected
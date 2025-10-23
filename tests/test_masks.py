import pytest
from config import setup_test_masks_logger

# Создаем логгер для тестов
test_logger = setup_test_masks_logger()

from src.masks import get_mask_account, get_mask_card_number

"""Тесты для get_mask_card_number"""


# Тесты для корректных номеров карт - ТОЛЬКО СТРОКИ
@pytest.mark.parametrize(
    "valid_card_number, expected_masks",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("1596837868705199", "1596 83** **** 5199"),
    ],
)
def test_get_mask_card_number_valid(valid_card_number: str, expected_masks: str) -> None:
    result = get_mask_card_number(valid_card_number)
    assert result == expected_masks


# ОТДЕЛЬНЫЙ тест для чисел (без parametrize)
def test_get_mask_card_number_with_int() -> None:
    """Тестируем что функция работает с числами"""
    result = get_mask_card_number(7000792289606361)
    assert result == "7000 79** **** 6361"


# Тесты для некорректных номеров карт
@pytest.mark.parametrize(
    "invalid_card_number",
    [
        "123456789012345",  # 15 цифр
        "12345678901234567",  # 17 цифр
        "1234abcd56789012",  # с буквами
        "1234-5678-9012-3456",  # с дефисами
        "",  # пустая строка
        "    ",  # только пробелы
        "1234 5678 1234",  # неполный номер
    ],
)
def test_get_mask_card_number_invalid(invalid_card_number: str) -> None:
    with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
        get_mask_card_number(invalid_card_number)


"""Тесты для get_mask_account"""


# Тесты для get_mask_account - ТОЛЬКО СТРОКИ
@pytest.mark.parametrize(
    "account_number, expected_mask",
    [
        ("35383033474447895560", "**5560"),
        ("73654108430135874305", "**4305"),
        ("64686473678894779589", "**9589"),
    ],
)
def test_get_mask_account_valid(account_number: str, expected_mask: str) -> None:
    result = get_mask_account(account_number)
    assert result == expected_mask


# ОТДЕЛЬНЫЙ тест для чисел (без parametrize)
def test_get_mask_account_with_int() -> None:
    """Тестируем что функция работает с числами"""
    result = get_mask_account(35383033474447895560)
    assert result == "**5560"


# Тесты для некорректных номеров счетов
@pytest.mark.parametrize(
    "invalid_account_number",
    [
        "1234567890123456789",  # 19 цифр
        "123456789012345678999999",  # 22 цифр
        "1234567890qwerty",  # с буквами
        "1234-5678-9012-3456-7890",  # дефисы
        "",  # пустая
        "      ",  # только пробелы
        "1234 5678 9012 3456",  # неполный формат
    ],
)
def test_get_mask_account_invalid(invalid_account_number: str) -> None:
    with pytest.raises(ValueError, match="Номер счета должен содержать 20 цифр"):
        get_mask_account(invalid_account_number)

import pytest

from src.masks import get_mask_account, get_mask_card_number


# Тесты для get_mask_card_number
@pytest.mark.parametrize(
    "card_number, expected_mask",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("1596837868705199", "1596 83** **** 5199"),
        # Ввод с пробелами внутри строки
        ("7000 7922 8960 6361", "7000 79** **** 6361"),
        (" 7000 7922 8960 6361 ", "7000 79** **** 6361"),
    ],
)
def test_get_mask_card_number_valid(card_number: str, expected_mask: str) -> None:
    result = get_mask_card_number(card_number)
    assert result == expected_mask


# Тесты для get_mask_account
@pytest.mark.parametrize(
    "account_number, expected_mask",
    [
        ("35383033474447895560", "**5560"),
        ("73654108430135874305", "**4305"),
        ("64686473678894779589", "**9589"),
        # Формат с пробелами
        ("3538 3033 4744 4789 5560", "**5560"),
        ("  3538 3033 4744 4789 5560  ", "**5560"),
    ],
)
def test_get_mask_account_valid(account_number: str, expected_mask: str) -> None:
    result = get_mask_account(account_number)
    assert result == expected_mask


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
    with pytest.raises(ValueError):
        get_mask_account(invalid_account_number)


def test_get_mask_card_number_empty_string() -> None:
    with pytest.raises(ValueError):
        get_mask_card_number("")


def test_get_mask_account_empty_string() -> None:
    with pytest.raises(ValueError):
        get_mask_account("")

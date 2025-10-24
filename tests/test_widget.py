import pytest

from src.widget import get_date, mask_account_card


# Тестирование функции mask_account_card
@pytest.mark.parametrize(
    "account_card, expected",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Visa Classic 6831982476737658", "Visa 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa 8990 92** **** 5229"),
        ("Visa Gold 5999414228426353", "Visa 5999 41** **** 6353"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_valid(account_card: str, expected: str) -> None:
    result = mask_account_card(account_card)
    assert result == expected


@pytest.mark.parametrize(
    "invalid_account_card",
    [
        "Maestro 15968378687099",  # меньше символов
        "Счет 6468647367889477958900",  # больше символов
        "MasterCard   ",
        "Счет 3538303347444789qq60",
        "",  # Пустая строка
        "Visa Platinum 8990-9221-1366-5229",
    ],
)
def test_mask_account_card_invalid(invalid_account_card: str) -> None:
    with pytest.raises(ValueError):
        mask_account_card(invalid_account_card)


def test_get_date_normal_cases():
    """Тестируем нормальные случаи работы функции"""
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"
    assert get_date("2023-10-05") == "05.10.2023"


def test_get_date_empty_string():
    """Тестируем пустую строку"""
    assert get_date("") == "Дата не указана"


def test_get_date_bad_formats():
    """Тестируем неправильные форматы"""
    assert get_date("bad-date") == "Неправильный формат"
    assert get_date("2024-03") == "Неправильный формат"
    assert get_date("abc") == "Неправильный формат"

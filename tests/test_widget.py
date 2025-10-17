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


# Тестирование функции get_date
@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-10-05", "05.10.2023"),
        ("", "Дата не указана"),
        ("bad-date", "Неправильный формат"),
        ("2024-02-30", "Неправильный формат"),  # некорректная дата
        ("2024-13-01", "Неправильный формат"),  # некорректный месяц
        # Можно добавить еще тесты
    ],
)
def test_get_date_errors(date_str: str, expected: str) -> None:
    result = get_date(date_str)
    assert result == expected

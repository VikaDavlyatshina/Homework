import pytest
from src.masks import get_mask_card_number, get_mask_account


#Тесты для функции маскировки номеров карт

def test_mask_card_number_basic():
        """Тест на стандартные данные без пробелов"""
        assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"
        assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"

def test_mask_card_with_spaces():
        """Тест с пробелами во входных данных"""
        assert get_mask_card_number("7000 7922 8960 6361") == "7000 79** **** 6361"
        assert get_mask_card_number("12 34 56 78 90 12 34 56") == "1234 56** **** 3456"

def test_mask_card_number_as_integer():
        """Тест номера карты как целого числа"""
        assert get_mask_card_number(7000792289606361) == "7000 79** **** 6361"
        assert get_mask_card_number(1234567890123456) == "1234 56** **** 3456"

def test_mask_card_number_too_short():
        """Тест на короткий номер карты"""
        with pytest.raises(ValueError) as exc_info:
            get_mask_card_number("123456789012345")
        assert str(exc_info.value) == "Номер карты должен содержать 16 цифр"

def test_mask_card_number_too_long():
        """Тест на длинный номер карты"""
        with pytest.raises(ValueError) as exc_info:
            get_mask_card_number("123456789012345678")
        assert str(exc_info.value) == "Номер карты должен содержать 16 цифр"

def test_mask_card_number_with_letters():
        """Тест на номер с буквами"""
        with pytest.raises(ValueError) as exc_info:
            get_mask_card_number("1234567890qwerty")
        assert str(exc_info.value) == "Номер карты должен содержать 16 цифр"

def test_mask_card_number_only_spaces():
        """Тест номера карты только с пробелами"""
        with pytest.raises(ValueError) as exc_info:
            get_mask_card_number("      ")
        assert str(exc_info.value) == "Номер карты должен содержать 16 цифр"


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1596837868705199", "1596 83** **** 5199"),
        ("7158300734726758", "7158 30** **** 6758"),
        ("8990922113665229", "8990 92** **** 5229"),
        ("5999414228426353", "5999 41** **** 6353"),
    ],
)
def test_mask_card_number_parametrized_valid(card_number, expected):
    """Параметризованный тест для правильных номеров карт"""
    assert get_mask_card_number(card_number) == expected


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
def test_card_number_parametrized_invalid(invalid_card_number):
    """Параметризованный тест для невалидных номеров карт"""
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number(invalid_card_number)
    assert str(exc_info.value) == "Номер карты должен содержать 16 цифр"


#Тесты для функции маскировки номера счета

def test_mask_account_basic():
    """Тест на стандартные данные без пробелов"""
    assert get_mask_account("35383033474447895560") == "**5560"
    assert get_mask_account("73654108430135874305") == "**4305"


def test_mask_account_with_spaces():
    """Тест с пробелами во входных данных"""
    assert get_mask_account("3538 3033 4744 4789 5560") == "**5560"
    assert get_mask_account("73 65 41 08 43 01 35 87 43 05") == "**4305"


def test_mask_account_as_integer():
    """Тест номера карты как целого числа"""
    assert get_mask_account(35383033474447895560) == "**5560"
    assert get_mask_account(73654108430135874305) == "**4305"


def test_mask_account_too_short():
    """Тест на короткий номер карты"""
    with pytest.raises(ValueError) as exc_info:
        get_mask_account("1234567890123456789")
    assert str(exc_info.value) == "Номер счета должен содержать 20 цифр"


def test_mask_account_too_long():
    """Тест на длинный номер карты"""
    with pytest.raises(ValueError) as exc_info:
        get_mask_account("123456789012345678999999")
    assert str(exc_info.value) == "Номер счета должен содержать 20 цифр"

def test_mask_account_with_letters():
    """Тест на номер с буквами"""
    with pytest.raises(ValueError) as exc_info:
        get_mask_account("35383033474447895qwe")
    assert str(exc_info.value) == "Номер счета должен содержать 20 цифр"


def test_account_only_spaces():
    """Тест номера карты только с пробелами"""
    with pytest.raises(ValueError) as exc_info:
        get_mask_account("      ")
    assert str(exc_info.value) == "Номер счета должен содержать 20 цифр"


@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("64686473678894779589", "**9589"),
        ("35383033474447895560", "**5560"),
        ("73654108430135874305", "**4305"),],
)
def test_mask_account_parametrized_valid(account_number, expected):
    """Параметризованный тест для правильных счетов"""
    assert get_mask_account(account_number) == expected

@pytest.mark.parametrize(
    "invalid_account_number",
    [
        "1234567890123456789",  # 19 цифр
        "123456789012345678901",  # 21 цифр
        "12345678901234567qwe",  # с буквами
        "1234-5678-9012-3456-7890",  # с дефисами
        "",  # пустая строка
        "    ",  # только пробелы
        "1234 5678 9012 3456",  # неполный номер
    ],
)
def test_account_parametrized_invalid(invalid_account_number):
    """Параметризованный тест для невалидных номеров карт"""
    with pytest.raises(ValueError) as exc_info:
        get_mask_account(invalid_account_number)
    assert str(exc_info.value) == "Номер счета должен содержать 20 цифр"


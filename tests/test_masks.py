import pytest
from src.masks import get_mask_card_number, get_mask_account

def test_get_mask_card_number_basic():
    """Тест базовой функциональности"""

assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"
assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"

def test_get_mask_card_number_errors():
    """Тест на короткий номер карты"""
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number("123456789012345")

    """Тест на номер с буквами"""
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number("1234567890qwerty")
    """Тест на длинный номер"""
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number("123456789012345678")

    # Проверяем, что сообщение об ошибке соответствует ожидаемому
    assert str(exc_info.value) == "Номер карты должен содержать 16 цифр"

def test_get_mask_card_with_spaces():
    """Тест с пробелами во входных данных"""
    assert get_mask_card_number("7000 7922 8960 6361") == "7000 79** **** 6361"
    assert get_mask_card_number("12 34 56 78 90 12 34 56") == "1234 56** **** 3456"

@pytest.mark.parametrize("card_number, expected", [("1596837868705199", "1596 83** **** 5199"),
                                                   ("7158300734726758", "7158 30** **** 6758"),
                                                   ("8990922113665229", "8990 92** **** 5229"),
                                                   ("5999414228426353", "5999 41** **** 6353")])
def test_get_mask_card(card_number, expected):
    assert get_mask_card_number(card_number) == expected
from src.masks import get_mask_card_number, get_mask_account


def test_get_mask_card_number():
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"




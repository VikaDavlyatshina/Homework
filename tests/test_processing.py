import pytest
from src.processing import filter_by_state, sort_by_date

def test_filter_by_state_default_with_fixture(example_of_transactions):
    #Тест базовой функциональности
    result = filter_by_state(example_of_transactions)
    expected_ids = [41428829, 939719570]
    assert [transaction['id'] for transaction in result] == expected_ids

def test_filter_by_state_with_fixture(example_of_transactions):
    #Тест на сортировку по другому ключу
    result = filter_by_state(example_of_transactions, "CANCELED")
    expected_ids = [594226727, 615064591]
    assert [transaction['id'] for transaction in result] == expected_ids

def test_filter_by_state_nonexistent_with_fixture(example_of_transactions):
    #Тест на сортировку по несуществующему ключу
    result = filter_by_state(example_of_transactions, "PENDING")
    assert result == []

def test_filter_by_state_empty():
    #Тест на пустой список
    result = filter_by_state([])
    assert result == []

def test_sort_by_date_with_fixture(example_of_transactions):
    result = sort_by_date(example_of_transactions)
    # Проверяем, что список отсортирован так, как ожидается(по убыванию)
    assert [transaction['id'] for transaction in result] == [41428829, 615064591, 594226727, 939719570]

def test_sort_by_date_ascending_with_fixture(example_of_transactions):
    result = sort_by_date(example_of_transactions, reverse=False)
    # Проверяем, что список отсортирован по возрастанию
    assert [transaction['id'] for transaction in result] == [939719570, 594226727, 615064591, 41428829]
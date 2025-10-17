from typing import Any, Dict, List


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Функция принимает список словарей и опционально значения для ключа state.
    Возвращает новый список словарей, содержащий те словари, у которых значение равно ключу state."""

    filtered_transactions = []
    for transaction in transactions:
        if transaction.get("state") == state:
            filtered_transactions.append(transaction)
    return filtered_transactions


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """Функция принимает список словарей и параметр, задающий порядок сортировки.
    Возвращает новый отсортированный список"""

    sorted_transactions_by_date = sorted(transactions, key=lambda x: x["date"], reverse=reverse)
    return sorted_transactions_by_date

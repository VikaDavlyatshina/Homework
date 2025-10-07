from typing import List, TypedDict


class Transaction(TypedDict):
    id: int
    state: str
    date: str


def filter_by_state(transactions: List[Transaction], state: str = "EXECUTED") -> List[Transaction]:
    """Функция принимает список словарей и опционально значения для ключа state.
    Возвращает новый список словарей, содержащий те словари, у которых значение равно ключу state."""

    filtered_transactions = []
    for transaction in transactions:
        if transaction.get("state") == state:
            filtered_transactions.append(transaction)
    return filtered_transactions


def sort_by_date(transactions: List[Transaction], reverse: bool = True) -> List[Transaction]:
    """Функция принимает список словарей и параметр, задающий порядок сортировки.
    Возвращает новый отсортированный список"""

    sorted_transactions_by_date = sorted(transactions, key=lambda x: x["date"], reverse=reverse)
    return sorted_transactions_by_date

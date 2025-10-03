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


data = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

print(filter_by_state(data, state="CANCELED"))
print(filter_by_state(data))
print(sort_by_date(data))
print(sort_by_date(data, reverse=False))
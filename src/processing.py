def filter_by_state(transactions: list[dict], state="EXECUTED") -> list[dict]:
    """Функция принимает список словарей и опционально значения для ключа state.
    Возвращает новый список словарей, содержащий те словари, у которых значение равно ключу state."""

    sorted_transactions = [transaction for transaction in transactions if transaction.get("state") == state]
    return sorted_transactions


def sort_by_date(transactions: list[dict], reverse=True) -> list[dict]:
    """Функция принимает список словарей и параметр, задающий порядок сортировки.
    Возвращает новый отсортированный список"""

    sorted_transactions_by_date = sorted(transactions, key=lambda x: x["date"], reverse=reverse)
    return sorted_transactions_by_date

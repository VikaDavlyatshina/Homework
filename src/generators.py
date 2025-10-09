def filter_by_currency(transactions, currency_code):
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code", {}) == currency_code:
            yield transaction

def transaction_descriptions(transactions):
    for transaction in transactions:
        yield transaction.get("description", "Нет описания")

def card_number_generator(start, end):
    if start < 1:
        start = 1
    for number in range(start, end + 1):
        # Преобразуем число в строку с ведущими нулями с помощью метода zfill()
        number_str = str(number).zfill(16)
        # Разделяем строку на части по 4 символа
        parts = [number_str[i:i+4] for i in range(0, 16, 4)]
        # Объединяем части с пробелами
        yield " ".join(parts)



from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card: str) -> str:
    """Возвращает строку с маскированным номером."""

    if len(account_card) == 0:
        raise ValueError("Ошибка! Поле не может быть пустым")
    else:
        parts = account_card.split()
        type_str = parts[0]
        number = parts[-1]

        # Проверяем, является ли это счетом
        if type_str.lower() == "счет":
            masked_number = get_mask_account(number)
            return f"{type_str} {masked_number}"
        else:
            masked_number = get_mask_card_number(number)
            return f"{type_str} {masked_number}"


def get_date(date_str: str) -> str:
    """Функция принимает строку с датой и возвращает в формате ДД.ММ.ГГГГ"""
    # Исходная строка: "2024-03-11T02:26:18.671407"

    # 1. Проверяем пустую строку
    if date_str == "":
        return "Дата не указана"

    # 2. Пробуем разобрать дату
    try:
        # Разделяем дату и время через разделитель 'T' и получим первый элемент списка
        date_part = date_str.split("T")[0]  # Результат "2024-03-11"

        # Разбиваем дату на составляющие
        part = date_part.split("-")

        # 3. Проверяем, что получилось 3 части
        if len(part) != 3:
            return "Неправильный формат"

        # Извлекаем отдельные компоненты
        day = part[2]
        month = part[1]
        year = part[0]

        # 4. Форматируем дату
        date = f"{day}.{month}.{year}"

        return date

    except IndexError:
        return "Неправильный формат"

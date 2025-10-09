import datetime

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
    if not date_str:
        return "Дата не указана"
    """Функция принимает строку с датой и возвращает в формате ДД.ММ.ГГГГ"""
    try:
        # 1. Преобразуем строку в объект datetime
        date = datetime.datetime.fromisoformat(date_str)  # Для формата ISO (2024-03-11T02:26:18.671407)

        # 2. Форматируем в ДД.ММ.ГГГГ
        formatted_date = date.strftime("%d.%m.%Y")
        return formatted_date
    except (ValueError, TypeError):
        return "Неправильный формат"

import logging
import os

# Создаем папку logs если она не существует
if not os.path.exists("logs"):
    os.makedirs("logs")

logger = logging.getLogger("masks")
logger.setLevel(logging.INFO)

# Создаем обработчик
file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

# добавляем обработчик, чтобы избежать дублирования
if not logger.hasHandlers():
    logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """ ""
    Маскирует номер карты.

    Args:
        card_number (int | str): Номер карты.

    Returns:
        str: Маскированный номер карты.

    Raises:
        ValueError: Если номер карты не 16 цифр или содержит недопустимые символы.
    """
    card_str = "".join(str(card_number).split())  # удаляем любые пробельные символы

    masked_for_log = "*" * (len(card_str) - 4) + card_str[-4:] if len(card_str) >= 4 else card_str
    logger.info(f"Начало маскировки номера карты: {masked_for_log}")

    if len(card_str) != 16:
        logger.error(f"Неверная длина номера карты: {len(card_number)} вместо 16")
        raise ValueError("Номер карты должен содержать 16 цифр")

    if not card_str.isdigit():
        logger.error(f"Номер карты содержит не только цифры: {card_number}")
        raise ValueError("Номер карты должен содержать 16 цифр")

    masked_card = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
    logger.info(f"Номер карты успешно замаскирован: {masked_card}")

    return masked_card


def get_mask_account(account_number: int | str) -> str:
    """
    Маскирует номер счета.

    Args:
        account_number (int | str): Номер счета.

    Returns:
        str: Маскированный номер счета.

    Raises:
        ValueError: Если номер счета не 20 цифр или содержит недопустимые символы.
    """
    account_str = "".join(str(account_number).split())

    masked_for_log = "*" * (len(account_str) - 4) + account_str[-4:] if len(account_str) >= 4 else account_str
    logger.info(f"Начало маскировки номера счета: {masked_for_log}")

    # Проверяем, что номер счета состоит из достаточного количества цифр
    if len(account_str) != 20:
        logger.error(f"Неверная длина номера счета: {len(account_str)} вместо 20")
        raise ValueError("Номер счета должен содержать 20 цифр")

    if not account_str.isdigit():
        logger.error("Номер счета должен содержать только цифры")
        raise ValueError("Номер счета должен содержать 20 цифр")

    masked_account = f"**{account_str[-4:]}"
    logger.info(f"Номер счета успешно замаскирован:{masked_account}")

    return masked_account

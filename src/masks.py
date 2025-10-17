import logging
import os

# Создаем папку logs если она не существует
if not os.path.exists('logs'):
    os.makedirs('logs')

logger = logging.getLogger("masks")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('logs/masks.log', mode='w', encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: int | str) -> str:
    """Функция, которая принимает номер карты и возвращает маску"""
    logger.info(f"Начало маскировки номера карты: {card_number}")

    card_number = str(card_number).replace(" ", "")

    if len(card_number) != 16:
        logger.error(f"Неверная длина номера карты: {len(card_number)} вместо 16")
        raise ValueError("Номер карты должен содержать 16 цифр")

    if not card_number.isdigit():
        logger.error(f"Номер карты содержит не только цифры: {card_number}")
        raise ValueError("Номер карты должен содержать только цифры")

    masked_card = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    logger.info(f"Номер карты успешно замаскирован: {masked_card}")

    return masked_card


def get_mask_account(account_number: int | str) -> str:
    """Функция принимает на вход номер счета возвращает маску"""
    logger.info(f"Начало маскировки номера счета: {account_number}")

    # Удаляем все пробелы из номера счета
    account_number = str(account_number).replace(" ", "")


    # Проверяем, что номер счета состоит из достаточного количества цифр
    if len(account_number) != 20:
        logger.error(f"Неверная длина номера счета: {len(account_number)} вместо 20")
        raise ValueError("Номер счета должен содержать 20 цифр")

    if not account_number.isdigit():
        logger.error("Номер счета должен содержать только цифры")
        raise ValueError("Номер счета должен содержать 20 цифр")

    masked_account =  f"**{account_number[-4:]}"
    logger.info(f"Номер счета успешно замаскирован:{masked_account}")

    return masked_account



if __name__ == "__main__":
    try:
        print(get_mask_card_number("1234 5678 9012 3456"))
    except ValueError as e:
        print(e)

    try:
        print(get_mask_account("12345678901234567890"))
    except ValueError as e:
        print(e)

    # Ошибочные случаи
    try:
        print(get_mask_card_number("123"))
    except ValueError as e:
        print(e)

    try:
        print(get_mask_account("1234567890123456789a"))
    except ValueError as e:
        print(e)

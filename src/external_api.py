import os
from typing import Optional

import requests
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

APIKEY = os.getenv("API_KEY")  # Получение токена API
EXCHANGE_API_URL = "https://api.apilayer.com/exchangerates_data/convert"


def converting_a_transactions_into_rub(transaction: dict) -> Optional[float]:
    """Функция принимает на вход транзакцию и возвращает сумму транзакций (amount) в рублях"""

    if not APIKEY:
        print("API_KEY не найден в переменных окружения")
        return None
    try:
        # Извлекаем сумму и код валюты
        amount = float(transaction["operationAmount"]["amount"])
        currency_code = transaction["operationAmount"]["currency"]["code"]

        if currency_code == "RUB":
            return amount

        if currency_code in ["USD", "EUR"]:
            headers = {"apikey": APIKEY}
            params = {"from": currency_code, "to": "RUB", "amount": amount}

            response = requests.get(EXCHANGE_API_URL, headers=headers, params=params)
            if response.status_code != 200:
                print(f"Ошибка API с кодом {response.status_code}: {response.text} ")
                return None

            data = response.json()
            if "result" in data:
                return float(data["result"])

            else:
                print(f"Некорректный ответ API: {data}")
                return None
        else:
            print(f"Неподдерживаемая валюта: {currency_code}")
            return None

    except KeyError as e:
        print(f"Отсутствует обязательное поле в транзакции: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка обращения к API: {e}")
        return None

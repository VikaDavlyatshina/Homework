import os
from dotenv import load_dotenv
import requests

# Загрузка переменных из .env файла
load_dotenv()

APIKEY = "MjvYNFpGpf8CKm40Ck1aP06zv9Vawrci"
# APIKEY = os.getenv('API_KEY') #Получение токена API
url= "https://api.apilayer.com/exchangerates_data/convert"

def convert_transactions_to_rub(transaction: dict) :
    """Функция принимает на вход транзакцию и возвращает сумму транзакций (amount) в рублях"""

    if not APIKEY:
        print("API_KEY не найден в переменных окружения")
        return None
    try:
        # Извлекаем сумму и код валюты
        amount = float(transaction["operationAmount"]["amount"])
        currency_code = transaction["operationAmount"]['currency']['code']

        if currency_code == 'RUB':
            return amount

        if currency_code in ['USD', 'EUR']:
            headers = {'apikey': APIKEY}
            params = {
                'from': currency_code,
                'to': 'RUB',
                'amount': amount
            }

            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            data = response.json()
            if 'result' in data:
                return  float(data['result'])

            else:
                print("Ошибка API: отсутствует 'result' в ответе.")
                return None
        else:
             print(f"Неподдерживаемая валюта: {currency_code}")
             return None

    except KeyError as e:
        print(f"Отсутствует обязательное поле в транзакции: {e}")
        return None
    except ValueError as e:
        print(f"Ошибка в преобразовании данных: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка обращения к API: {e}")
        return None










import os
from dotenv import load_dotenv
import requests

# Загрузка переменных из .env файла
load_dotenv()

#Получение токена API
APIKEY = os.getenv('API_KEY')
BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"

def get_sum_transactions(transaction: dict) -> float:
    """Функция принимает на вход транзакцию и возвращает сумму транзакций (amount) в рублях"""

    pass


    return amount
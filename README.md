# Проект Homework
## Описание:
Виджет, который показывает несколько последних успешных банковских операций клиента.
## Установка:
1. Клонируйте репозиторий:
```
git clone https://github.com/VikaDavlyatshina/Homework.git
```
2. Установите зависимости:
```
poetry install
```
## Тестирование
Проект использует `pytest` для написания и выполнения тестов. Чтобы запустить тесты, следуйте инструкциям ниже:
1. В корневой директории проекта выполните команду для запуска всех тестов:
`pytest`
2. Если необходимо, вы можете указать конкретный файл теста:
`pytest tests/test_example.py`
Это позволит убедиться, что проект работает корректно и все функции проходят проверку.

### Генераторы для транзакций
Новый модуль `genetators` представляет инструменты для обработки списка транзакций и генерации данных. Генераторы 
позволяют обрабатывать большие данные не загружая весь набор данных в память, что особенно полезно для оптимизации 
производительности и экономии ресурсов при анализе большого количества транзакций.
#### `filter_by_currency`
Функция `filter_by_currency` создаёт генератор, который итерируется по списку транзакций и выдаёт транзакции, соответствующие
заданной валюте.

**Параметры:**
* transactions - список словарей с транзакциями
* currency - код валюты(например, "USD")

**Возвращает:**
Итератор словарей, где каждая транзакция имеет указанную валюту.
**Пример использования**
```python
from src.generators import filter_by_currency
 
transactions =[
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        }]
# Получение генератора для транзакций в USD
usd_transaction_gen =filter_by_currency(transactions, "USD")
# Итерация по генератору
print("Транзакции в USD")
for transactions in usd_transaction_gen:
    print(transactions)
```
### Декоратор log
Новый модуль `decorators` содержит декоратор `@log`. Декоратор автоматически логирует успешное выполнение функции 
или ошибки, возникающие во время её вызова. Можно указывать файл для записи логов, либо вывести результат в консоль.
**Пример использования**
```python
from src.decorators import log
@log(filename='log.txt')
def my_function():
     print("Hello!")

@log()
def another_func():
    raise ValueError("Ошибка!")
```
### Работа с файлами и валютами
Новые модули `utils` и `file_readers` предоставляют инструменты для считывания информации о транзакциях из файлов разных
форматов. Функции позволяют загружать данные о транзакциях из файлов в формате JSON, CSV, Excel соответственно.
Каждая функция возвращает список словарей, где каждый словарь - одна транзакция.

**Функции**
* read_transactions_from_json(file_path: str) -> List[Dict[str, Any]]
* read_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]
* read_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]

**Пример использования**
```python
from src.utils import read_transactions_from_json

json_transactions = read_transactions_from_json('data/operations.json')

```
Также в модуле `external_api` реализована функция для конвертации суммы в рубли с помощью обращения к внешнему API:
* def converting_a_transactions_into_rub(transaction: dict) -> Optional[float]:
Функция принимает на вход транзакцию и возвращает сумму транзакций в рублях `RUB`. Если транзакция указана в `USD` или 
в `EUR`, происходит обращение к внешнему API для получения текущего курса валют и конвертации сумму в рубли.
```python
from src.external_api import converting_a_transactions_into_rub

# Пример транзакции в долларах
transaction_usd = {
    "operationAmount": {
        "amount": "150.00",
        "currency": {
            "code": "USD"
        }
    }
}

# Конвертация суммы в рубли
rub_amount = converting_a_transactions_into_rub(transaction_usd)

if rub_amount is not None:
    print(f"Сумма операции в рублях: {rub_amount:.2f} RUB")
else:
    print("Не удалось конвертировать сумму")
```

Важно: Для корректной работы функции необходимо:

* Создать файл .env с переменной API_KEY, содержащей ваш API-ключ;
* Установить зависимости: requests и python-dotenv
# Проект Homework
## Описание:
Виджет, который показывает несколько последних успешных банковских операций клиента.
Основная задача проекта: подготовка и обработка данных о транзакциях для их последующего отображения в интерфейсе.
## Функциональность
- **Чтение данных:** загрузка информации о транзакциях из файлов различных форматов(JSON, EXCEL, CSV)
- **Фильтрация:** генератор для фильтрации транзакций по валюте
- **Поиск по описанию:** Поиск транзакций по ключевым словам в описании операции
- **Статистика по категориям**: Подсчет количества операций по категориям/типам транзакций
- **Конвертация валют**: Автоматическая конвертация сумм операций в рубли (RUB) через внешнее API
- **Логирование**: Декоратор для автоматического логирования работы функций
- **Сортировка и фильтрация**: Сортировка по дате, фильтрация по статусу операции

## Установка:
1. Клонируйте репозиторий:
```
git clone https://github.com/VikaDavlyatshina/Homework.git
```
2. Установите зависимости с помощью Poetry:
```
poetry install
```
3. Настройка переменного окружения(для работы с API):
 Создайте файл .env в корне проекта и добавьте ваш API-ключ:
```
 API_KEY=ваш_ключ_от_API
 ```

## Тестирование
Проект использует `pytest` для написания и выполнения тестов. Чтобы запустить тесты, следуйте инструкциям ниже:
1. В корневой директории проекта выполните команду для запуска всех тестов:
`pytest`
2. Если необходимо, вы можете указать конкретный файл теста:
`pytest tests/test_example.py`
Это позволит убедиться, что проект работает корректно и все функции проходят проверку.

## Использование:

### 1. Работа с файлами(Модули utils и file_readers)
Для работы с файлами в проекте есть два модуля. Модуль `utils` содержит инструмент для чтения файлов в формате JSON.
Модуль `file_readers` инструменты для чтения файлов в формате CSV и Excel. Функции позволяют загружать данные о транзакциях
из файлов в формате JSON, CSV, Excel соответственно. Каждая функция возвращает список словарей, где каждый словарь - одна транзакция.

**Функции**
* read_transactions_from_json(file_path: str) -> List[Dict[str, Any]]
* read_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]
* read_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]

**Пример использования**: Загрузка из файлов
```python
from src.utils import read_transactions_from_json
from src.file_readers import read_transactions_from_csv, read_transactions_from_excel

# Загрузка из JSON
transactions_json = read_transactions_from_json('data/operations.json')

# Загрузка из CSV
transactions_csv = read_transactions_from_csv('data/transactions.csv')

# Загрузка из Excel
transactions_excel = read_transactions_from_excel('data/transactions_excel.xlsx')
```

### 2. Генераторы для транзакций(Модуль generators)
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
### 3. Декоратор log (Модуль decorators)
Модуль `decorators` содержит декоратор `@log`. Декоратор автоматически логгирует успешное выполнение функции 
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

### 4. Работа с валютами (Модуль external_api)
В модуле `external_api` реализована функция для конвертации суммы в рубли с помощью обращения к внешнему API:

* def converting_a_transactions_into_rub(transaction: dict) -> Optional[float]:

* Функция принимает на вход транзакцию и возвращает сумму транзакций в рублях `RUB`. Если транзакция указана в `USD` или 
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

### 5. Поиск по описанию транзакций(Модуль bank_functions)
Функция `process_bank_search` выполняет поиск транзакций по ключевому слову в описании операции с использованием регулярных выражений.

**Параметры:**

* data - список словарей с транзакциями
* search - строка для поиска в описании

**Возвращает:** Список транзакций, содержащих указанную строку в описании

**Пример использования:**
```python
from src.bank_functions import process_bank_search

transactions = [
    {
        "id": 1,
        "description": "Перевод организации",
        "amount": "1000.00",
        "currency": "RUB"
    },
    {
        "id": 2,
        "description": "Оплата услуг связи", 
        "amount": "500.00",
        "currency": "RUB"
    },
    {
        "id": 3,
        "description": "Перевод между счетами",
        "amount": "2000.00", 
        "currency": "RUB"
    },
    {
        "id": 4,
        "description": "Оплата интернета",
        "amount": "300.00",
        "currency": "RUB"
    }
]

# Поиск транзакций со словом "Перевод"
transfer_transactions = process_bank_search(transactions, "Перевод")
print(f"Найдено {len(transfer_transactions)} транзакций с 'Перевод':")
for transaction in transfer_transactions:
    print(f"- {transaction['description']}: {transaction['amount']} {transaction['currency']}")

# Поиск транзакций со словом "Оплата"
payment_transactions = process_bank_search(transactions, "Оплата")
print(f"\nНайдено {len(payment_transactions)} транзакций с 'Оплата':")
for transaction in payment_transactions:
    print(f"- {transaction['description']}: {transaction['amount']} {transaction['currency']}")
```

**Вывод:**
```text
Найдено 2 транзакций с 'Перевод':
- Перевод организации: 1000.00 RUB
- Перевод между счетами: 2000.00 RUB

Найдено 2 транзакций с 'Оплата':
- Оплата услуг связи: 500.00 RUB
- Оплата интернета: 300.00 RU
```
**Особенности:**

* Поиск без учета регистра

* Использование регулярных выражений для точного поиска

* Экранирование специальных символов

### 6. Основное положение
Для запуска интерактивного режима работы с транзакциями:

```bash
python main.py
```


**Программа предоставит пошаговое меню для**:

* Выбора источника данных (JSON/CSV/Excel)

* Фильтрации по статусу операции

* Сортировки по дате

* Фильтрации по валюте

* Поиска по описанию

* Просмотра статистики

* Сохранения результатов
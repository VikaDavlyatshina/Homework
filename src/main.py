from config import CSV_FILE, EXCEL_FILE, JSON_FILE
from src.bank_functions import process_bank_search
from src.file_readers import read_transactions_from_csv, read_transactions_from_excel
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.utils import read_transactions_from_json
from src.widget import get_date, mask_account_card


def main() -> None:  # pragma: no cover
    """Отвечает за основную логику проекта и связывает функциональности между собой"""

    print("Привет, добро пожаловать в программу работы с банковскими транзакциями")
    print("Выберите необходимый пункт в меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из Excel-файла")

    while True:
        try:
            user_choice = int(input("Введите нужную цифру: "))
            if user_choice in [1, 2, 3]:
                break
            else:
                print("Пожалуйста введите 1, 2 или 3")
        except ValueError:
            print("Это должно быть число! Попробуйте снова.")

    transactions = None

    # Загружаем данные в зависимости от выбора
    if user_choice == 1:
        print("Для обработки выбран JSON-файл")
        transactions = read_transactions_from_json(str(JSON_FILE))
    elif user_choice == 2:
        print("Для обработки выбран CSV-файл")
        transactions = read_transactions_from_csv(str(CSV_FILE))
    elif user_choice == 3:
        print("Для обработки выбран Excel-файл")
        transactions = read_transactions_from_excel(str(EXCEL_FILE))

    # Проверяем, загрузились ли данные
    if not transactions:
        print("Не удалось загрузить данные из файла")
        return

    print(f"Загружено {len(transactions)} транзакций")

    # 2. Фильтрация по статусу
    print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
    print("Доступные для фильтрации статусы: EXECUTED, CANCELED, PENDING")

    while True:
        status_input = input("Введите статус: ").upper()
        if status_input in ["EXECUTED", "CANCELED", "PENDING"]:
            break
        else:
            print(f"Статус {status_input} недоступен! Выберите статус из перечисленных")

    # Фильтруем операцию по статусу
    filtered_transactions = filter_by_state(transactions, state=status_input)
    print(f"Операции отфильтрованы по статусу '{status_input}'")
    print(f"После фильтрации осталось {len(filtered_transactions)} транзакций")

    # Проверяем, остались ли транзакции после фильтрации
    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # 3. Сортировка по дате
    while True:
        print("\nОтсортировать операции по дате? Да/Нет")
        user_input = input("Введите 'Да' или 'Нет' ").strip().lower()

        if user_input in ["д", "да", "yes", "y", "1"]:
            # Начинаем сортировку
            while True:
                try:
                    sort_direction = int(
                        input(
                            "Поставьте необходимое число:\n" "1 - по возрастанию\n" "2 - по убыванию\n" "Ваш выбор: "
                        )
                    )
                    if sort_direction in [1, 2]:
                        break
                    else:
                        print("Введите 1 или 2")
                except ValueError:
                    print("Это должно быть число! Введите 1 или 2")

            # Сортируем транзакции
            if sort_direction == 1:
                filtered_transactions = sort_by_date(filtered_transactions, reverse=False)  # По возрастанию
                print("Операции отсортированы по возрастанию")
            else:
                filtered_transactions = sort_by_date(filtered_transactions)  # По убыванию
                print("Операции отсортированы по убыванию")
            break  # Выход из цикла после выполнения сортировки
        elif user_input in ["нет", "н", "no", "n", "2"]:
            print("Сортировка по дате пропущена.")
            break  # Выход из цикла без сортировки
        else:
            # Некорректный ввод - повторяем запрос
            print("Пожалуйста введите 'Да' или 'Нет'.")

    # 4. Фильтрация по валюте
    while True:
        print("\nВыводить только рублевые транзакции? Да/Нет")
        currency_choice = input("Сделайте выбор: ").strip().lower()

        if currency_choice in ["да", "д", "yes", "y", "1"]:
            filtered_transactions = list(filter_by_currency(filtered_transactions, "RUB"))
            print("Оставлены только рублевые транзакции")
            break
        elif currency_choice in ["нет", "н", "no", "n", "2"]:
            print("Вывод транзакций по всем валютам.")
            break
        else:
            # Некорректный ввод - повторяем запрос
            print("Пожалуйста введите 'Да' или 'Нет'.")

    # 5. ПОИСК ПО ОПИСАНИЮ
    while True:
        print("\nХотите отфильтровать транзакции по слову в описании? Да/Нет")
        search_choice = input("Ваш выбор: ").strip().lower()

        if search_choice in ["да", "д", "yes", "y", "1"]:
            search_word = input("Введите слово для поиска: ").strip()
            if search_word:
                filtered_transactions = process_bank_search(filtered_transactions, search_word)
                if filtered_transactions:
                    print(f"\nНайдено {len(filtered_transactions)} транзакций с словом '{search_word}'")
                else:
                    print(f"\nНет транзакций с словом '{search_word}'.")
            else:
                print("Слово для поиска не введено.")
            break
        elif search_choice in ["нет", "н", "no", "n", "2"]:
            print("Фильтрация по слову не выполнена.")
            break
        else:
            print("Пожалуйста введите 'Да' или 'Нет'.")

    # 6. ПРОВЕРКА РЕЗУЛЬТАТОВ
    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # 7. ВЫВОД РЕЗУЛЬТАТОВ
    print("\nРаспечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(filtered_transactions)}\n")
    for i, transaction in enumerate(filtered_transactions, 1):
        print(f"Транзакция {i}\n")

        date = get_date(transaction.get("date", ""))
        descriptions = transaction.get("description", "Нет описания")
        print(f"{date} {descriptions}")

        from_account = transaction.get("from", "")
        if type(from_account) is float:
            from_account = ""
        to_account = transaction.get("to", "")

        if from_account and to_account:
            print(f"{mask_account_card(from_account)} -> {mask_account_card(to_account)}")
        elif to_account:
            print(f"{mask_account_card(to_account)}")

        if "operationAmount" in transaction:
            amount = transaction["operationAmount"]["amount"]
            currency = transaction["operationAmount"]["currency"]["name"]
        else:
            amount = transaction.get("amount", "0")
            currency = transaction.get("currency_name", "руб.")

        print(f"{amount} {currency}\n")


if __name__ == "__main__":
    main()

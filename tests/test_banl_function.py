from src.bank_functions import process_bank_search, process_bank_operations


class TestProcessBankSearch:
    """Тесты для функции поиска транзакций"""

    def test_search_found(self):
        """Тест: поиск находит транзакции"""
        # Подготовка тестовых данных
        test_data = [
            {"description": "Перевод в банк СБЕР", "amount": 100},
            {"description": "Оплата магазина", "amount": 200},
            {"description": "Перевод другу", "amount": 300},
        ]

        # Вызов функции
        result = process_bank_search(test_data, "Перевод")

        # Проверка результата
        assert len(result) == 2  # Должно найти 2 транзакции с "Перевод"
        assert result[0]["description"] == "Перевод в банк СБЕР"
        assert result[1]["description"] == "Перевод другу"

    def test_search_not_found(self):
        """Тест: поиск не находит транзакции"""
        test_data = [
            {"description": "Оплата магазина", "amount": 100},
            {"description": "Снятие наличных", "amount": 200},
        ]

        result = process_bank_search(test_data, "Перевод")

        # Должен вернуть пустой список
        assert result == []

    def test_search_case_insensitive(self):
        """Тест: поиск без учета регистра"""
        test_data = [{"description": "перевод в банк", "amount": 100}, {"description": "ПЕРЕВОД ДРУГУ", "amount": 200}]

        result = process_bank_search(test_data, "Перевод")

        # Должен найти обе транзакции, несмотря на разный регистр
        assert len(result) == 2

    def test_empty_data(self):
        """Тест: пустые входные данные"""
        result = process_bank_search([], "Перевод")
        assert result == []

    def test_empty_search_string(self):
        """Тест: пустая строка поиска"""
        test_data = [{"description": "Перевод в банк", "amount": 100}]

        result = process_bank_search(test_data, "")

        # При пустом поиске должна вернуть все транзакции
        assert len(result) == 1


class TestProcessBankOperations:
    """Тесты для функции подсчета операций по категориям"""

    def test_count_operations(self):
        """Тест: подсчет операций по категориям"""
        test_data = [
            {"description": "Перевод в СБЕР", "amount": 100},
            {"description": "Оплата Магнит", "amount": 200},
            {"description": "Перевод в Тинькофф", "amount": 300},
            {"description": "Оплата Пятерочка", "amount": 400},
        ]

        categories = ["Перевод", "Оплата"]

        result = process_bank_operations(test_data, categories)

        # Проверяем подсчет
        assert result["Перевод"] == 2  # 2 операции с "Перевод"
        assert result["Оплата"] == 2  # 2 операции с "Оплата"

    def test_count_no_matches(self):
        """Тест: нет совпадений по категориям"""
        test_data = [
            {"description": "Снятие наличных", "amount": 100},
            {"description": "Пополнение счета", "amount": 200},
        ]

        categories = ["Перевод", "Оплата"]

        result = process_bank_operations(test_data, categories)

        # Все категории должны быть 0
        assert result["Перевод"] == 0
        assert result["Оплата"] == 0

    def test_count_case_insensitive(self):
        """Тест: подсчет без учета регистра"""
        test_data = [{"description": "перевод в банк", "amount": 100}, {"description": "ПЕРЕВОД ДРУГУ", "amount": 200}]

        categories = ["Перевод"]

        result = process_bank_operations(test_data, categories)

        # Должен посчитать обе транзакции
        assert result["Перевод"] == 2

    def test_empty_data(self):
        """Тест: пустые данные"""
        categories = ["Перевод", "Оплата"]

        result = process_bank_operations([], categories)

        # При пустых данных все категории должны быть 0
        assert result["Перевод"] == 0
        assert result["Оплата"] == 0

    def test_empty_categories(self):
        """Тест: пустой список категорий"""
        test_data = [{"description": "Перевод в банк", "amount": 100}]

        result = process_bank_operations(test_data, [])

        # Должен вернуть пустой словарь
        assert result == {}

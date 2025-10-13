import os
from functools import wraps
from typing import Callable, Generator, ParamSpec, TypeVar

import pytest

from src.decorators import log

# Объявляем параметр для параметров функции(аргументы и ключевые аргументы)
P = ParamSpec("P")

# Объявляем параметр для возвращаемого типа
T = TypeVar("T")


# Фикстура для удаления файла перед каждым тестом
@pytest.fixture(autouse=True)
def cleanup_file() -> Generator[None]:
    filename = "test_log.txt"
    if os.path.exists(filename):
        os.remove(filename)
    yield
    if os.path.exists(filename):
        os.remove(filename)


# Тест проверки вывода в консоль
def test_success_console(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def good_func() -> int:
        return 42

    good_func()
    out, _ = capsys.readouterr()
    assert "good_func успешно выполнена." in out


# Тест для проверки записи в файл
def test_success_file() -> None:
    filename = "test_log.txt"

    @log(filename)
    def good_func() -> int:
        return 42

    good_func()

    with open(filename, "r", encoding="utf8") as f:
        content = f.read()
    assert "good_func успешно выполнена." in content


# Тест вывода сообщения об ошибке в консоль
def test_error_console(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def bad_func() -> None:
        raise ValueError("ошибка")

    bad_func()
    out, _ = capsys.readouterr()
    assert "bad_func не выполнена." in out
    assert "ValueError" in out


# Тест записи вывода об ошибке в файл
def test_error_file() -> None:
    filename = "test_log.txt"

    @log(filename)
    def bad_func() -> None:
        raise RuntimeError("проблема")

    bad_func()

    with open(filename, "r", encoding="utf8") as f:
        content = f.read()
    assert "bad_func не выполнена." in content
    assert "RuntimeError" in content


# Тест проверки сохранения документации декоратором wraps


# Создаем декораторы для тестирования
def log_without_wraps(func: Callable[P, T]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        return func(*args, **kwargs)

    return wrapper


def log_with_wraps(func: Callable[P, T]) -> Callable[P, T]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        return func(*args, **kwargs)

    return wrapper


# Исходная функция для проверки
def func_add(a: int, b: int) -> int:
    """Функция сложения двух чисел"""
    return a + b


def test_wraps_preserves_metadata() -> None:
    wrapped_without = log_without_wraps(func_add)  # Оборачиваем без декоратора @wraps
    wrapped_with = log_with_wraps(func_add)  # Оборачиваем с декоратором @wraps

    # Проверка без wraps
    assert wrapped_without.__name__ == "wrapper"
    assert wrapped_without.__doc__ is None

    # Проверка с wraps
    assert wrapped_with.__name__ == "func_add"
    assert wrapped_with.__doc__ == "Функция сложения двух чисел"

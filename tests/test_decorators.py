import pytest
import os
from src.decorators import log  # замените на имя файла с декоратором

# Фикстура для удаления файла перед каждым тестом
@pytest.fixture(autouse=True)
def cleanup_file():
    filename = 'log.txt'
    if os.path.exists(filename):
        os.remove(filename)
    yield
    if os.path.exists(filename):
        os.remove(filename)

def test_success_console(capsys):
    @log()
    def good_func():
        return 42

    good_func()
    out, _ = capsys.readouterr()
    assert "good_func успешно выполнена." in out

def test_success_file():
    filename = 'log.txt'
    @log(filename)
    def good_func():
        return 42

    good_func()

    with open(filename, 'r', encoding='utf8') as f:
        content = f.read()
    assert "good_func успешно выполнена." in content

def test_error_console(capsys):
    @log()
    def bad_func():
        raise ValueError("ошибка")

    bad_func()
    out, _ = capsys.readouterr()
    assert "bad_func не выполнена." in out
    assert "ValueError" in out

def test_error_file():
    filename = 'log.txt'
    @log(filename)
    def bad_func():
        raise RuntimeError("проблема")

    bad_func()

    with open(filename, 'r', encoding='utf8') as f:
        content = f.read()
    assert "bad_func не выполнена." in content
    assert "RuntimeError" in content
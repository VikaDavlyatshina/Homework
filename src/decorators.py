def log(filename=None):
        """Декоратор, который пишет, успешно ли выполнена функция."""

        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    result = func(*args, **kwargs)
                    message = f"{func.__name__} успешно выполнена."
                    if filename:
                        with open(filename, 'a', encoding='utf8') as f:
                            f.write(message + '\n')
                    else:
                        print(message)
                    return result
                except Exception as e:
                    error_msg = f"{func.__name__} не выполнена. Ошибка: {type(e).__name__}."
                    if filename:
                        with open(filename, 'a', encoding='utf8') as f:
                            f.write(error_msg + '\n')
                    else:
                        print(error_msg)

            return wrapper

        return decorator

@log(filename="mylog.txt")
def my_function(x, y):
    return x + y

my_function(1, 2)

@log()  # Лог в консоль
def add(a, b):
    return a + b

@log(filename="logfile.txt")  # Лог в файл
def divide(a, b):
    return a / b

print(add(2, 3))
print(divide(4, 2))
print(divide(4, 0))
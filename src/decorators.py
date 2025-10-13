from functools import wraps

def log(filename=None):
        """Декоратор, который автоматически регистрирует детали выполнения функции."""

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    # При успешном выполнении функции, генерируется сообщение об успехе
                    result = func(*args, **kwargs)
                    message = f"{func.__name__} успешно выполнена."

                    if filename:
                        # Если указан файл, записываем результат работы функции в указанный файл
                        with open(filename, 'a', encoding='utf8') as f:
                            f.write(message + '\n')
                    else:
                        # Если файл не указан, выводим сообщение в консоль
                        print(message)
                    return result
                except Exception as e:
                    # Генерируется сообщение об ошибке
                    error_msg = f"{func.__name__} не выполнена. Ошибка: {type(e).__name__}."
                    if filename:
                        # Если файл указан, информация об ошибке записывается в файл
                        with open(filename, 'a', encoding='utf8') as f:
                            f.write(error_msg + '\n')
                    else:
                        # Иначе выводится в консоль
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

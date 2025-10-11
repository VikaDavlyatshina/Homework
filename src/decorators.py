import functools


def log(filename=None):
    def my_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
                try:
                    #Выполняем функцию
                    result = func(*args, **kwargs)
                    # Формируем сообщение об успехе
                    success_message = f"{func.__name__} ок"
                    # Записываем в лог
                    if filename:
                        with open(filename, 'a', encoding='utf8') as file:
                            file.write(f"{success_message} \n")
                    else:
                        print(success_message)
                    return result
                except Exception as e:
                    # Формируем сообщение об ошибке
                    error_massage = f"{func.__name__} error: {type(e).__name__}. Inputs: {str(args)}, {str(kwargs)}."
                    # Записываем лог ошибки
                    if filename:
                        with open(filename, 'a', encoding='utf8') as file:
                            file.write(f"{error_massage}\n")
                    else:
                        print(error_massage)
                raise
        return wrapper
    return my_decorator


@log(filename="mylog.txt")
def my_function(x, y,):
    return x + y

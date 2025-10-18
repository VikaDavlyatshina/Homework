from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """Декоратор, который автоматически регистрирует детали выполнения функции."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                # При успешном выполнении функции, генерируется сообщение об успехе
                result = func(*args, **kwargs)
                message = f"{func.__name__} успешно выполнена."

                if filename:
                    # Если указан файл, записываем результат работы функции в указанный файл
                    with open(filename, "a", encoding="utf8") as f:
                        f.write(message + "\n")
                else:
                    # Если файл не указан, выводим сообщение в консоль
                    print(message)
                return result
            except Exception as e:
                # Генерируется сообщение об ошибке
                error_msg = f"{func.__name__} не выполнена. Ошибка: {type(e).__name__}."
                if filename:
                    # Если файл указан, информация об ошибке записывается в файл
                    with open(filename, "a", encoding="utf8") as f:
                        f.write(error_msg + "\n")
                else:
                    # Иначе выводится в консоль
                    print(error_msg)

        return wrapper

    return decorator

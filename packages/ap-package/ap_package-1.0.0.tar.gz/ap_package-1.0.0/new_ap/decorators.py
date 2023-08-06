# decorators.py
# decorators.py
import functools
# decorators.py
from loguru import logger


def log_call(level: str = 'INFO'):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.log(level, f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            logger.log(level, f"Function {func.__name__} returned {result}")
            return result

        return wrapper

    return decorator


# ... 其他装饰器 ...


def handle_exceptions(error_msg: str = '发生错误'):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"{error_msg}: {e}")

        return wrapper

    return decorator


# ... validate_io_config 装饰器 ...

def validate_io_config(func):
    def wrapper(*args, **kwargs):
        input_config, output_config = args[1], args[2]

        # 在这里验证输入配置参数对。如果有需要，您可以扩展这个验证逻辑。
        for key in input_config:
            if not hasattr(args[0].input_config, key):
                raise ValueError(f"{key} 不是有效的输入配置参数")

        # 在这里验证输出配置参数对。如果有需要，您可以扩展这个验证逻辑。
        for key in output_config:
            if not hasattr(args[0].output_config, key):
                raise ValueError(f"{key} 不是有效的输出配置参数")

        return func(*args, **kwargs)

    return wrapper

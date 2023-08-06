import logging
from functools import wraps
import time

loggers = {}


def setup_logger(name, log_level=logging.ERROR, log_file=None):
    global loggers

    if loggers.get(name):
        return loggers.get(name)

    else:
        logger = logging.getLogger(name)
        logger.setLevel(log_level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "file_name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}'
        )
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        loggers[name] = logger
        return logger


def timeit(logging):
    def operate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            logging.info(f'{func.__name__} finished in {(end - start):.2f}s')
            return result

        return wrapper

    return operate

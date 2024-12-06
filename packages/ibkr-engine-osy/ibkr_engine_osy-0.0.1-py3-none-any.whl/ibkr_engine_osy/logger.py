import logging
import pathlib
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CURRENT_DIR = Path(__file__).resolve().parent

LOGGING_FILE_NAME = 'logs.log'


class Logger:
    def __init__(self, _class):
        self.class_name: str = _class.__name__
        self._logger = logging.getLogger(name=self.class_name)
        formatter = logging.Formatter('%(levelname)s:: %(name)s: %(message)s')
        file_handler = logging.FileHandler(filename=LOGGING_FILE_NAME)
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

    def __call__(self, *, func=None, msg: str = '') -> None:
        if func is not None:
            func_name: str = func.__name__
            msg = f'at {func_name}: {msg}'
            self._logger.info(msg)
        self._logger.info(msg)

    def error(self, func=None, msg: str = '') -> None:
        if func is not None:
            func_name: str = func.__name__
            msg = f'at {func_name}: {msg}'
            self._logger.error(msg)
        self._logger.error(msg)

    def debug(self, *args, func=None, msg: str = '') -> None:
        if func is not None:
            func_name: str = func.__name__
            msg = f'at {func_name}: {msg}'
            self._logger.debug(msg, args)
        self._logger.debug(msg, args)

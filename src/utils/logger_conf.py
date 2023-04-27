import os
import sys
import traceback
import time
import logging as log

DEFAULT_FORMATTER = log.Formatter('[ %(levelname)s ] %(message)s')


class ColorFormatter(log.Formatter):

    grey = '\x1b[38;20m'
    yellow = '\x1b[33;20m'
    red = '\x1b[31;20m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'
    custom_format = '[ %(levelname)s ] %(message)s'

    FORMATS = {
        log.DEBUG: grey + custom_format + reset,
        log.WARNING: yellow + custom_format + reset,
        log.ERROR: red + custom_format + reset,
        log.CRITICAL: bold_red + custom_format + reset,
    }

    def format(self, record):   # noqa
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = log.Formatter(log_fmt)
        return formatter.format(record)


def exception_hook(exc_type, message, stack):   # noqa
    """
    Allows capturing uncaught exceptions to the log file.
    Usage: define sys.excepthook = exception_hook
    Warning: works only for the main thread.
    """
    log.error(f'Uncaught exception: {exc_type.__name__}: {message}.\nTraceback:\n'
              f'{"".join(traceback.format_tb(stack))}')


def configure_logger(name='', level=log.INFO, use_default_formatter=False):
    """
    Modifies logging: allows writing to log file with colored messages
    Usage: import logging, call configure_logger(), use logging as is
    :param name: logfile name (file format: <name>_<time>.log)
    :param level: logging level
    :param use_default_formatter: mark True to disable colored output
    :return:
    """
    log_time = time.strftime('%d%m_%I%M%S')
    log_path = os.path.join('logs', f'{name}_{log_time}.log')
    formatter = DEFAULT_FORMATTER if use_default_formatter else ColorFormatter()
    if not os.path.exists('logs'):
        os.makedirs('logs')

    stream_handler = log.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)

    file_handler = log.FileHandler(log_path)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    log.basicConfig(
        level=level,
        datefmt='%d/%m/%Y %I:%M:%S %p',
        handlers=[stream_handler, file_handler],
    )

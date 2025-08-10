import logging as log
import sys


DEFAULT_FORMATTER = log.Formatter('[ %(levelname)s ] %(message)s')


def configure_logger(name='', level=log.INFO, use_default_formatter=False):

    logger = log.getLogger()
    logger.setLevel(level)

    if logger.hasHandlers():
        logger.handlers.clear()

    stream_handler = log.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(level)
    stream_handler.setFormatter(DEFAULT_FORMATTER)
    logger.addHandler(stream_handler)

    file_handler = log.FileHandler(name, 'w')
    file_handler.setLevel(level)
    file_handler.setFormatter(DEFAULT_FORMATTER)
    logger.addHandler(file_handler)

    logger.propagate = False
    return logger

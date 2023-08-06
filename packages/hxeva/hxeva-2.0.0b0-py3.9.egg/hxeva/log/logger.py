# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/4/26   17:44
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ['CustomFormatter', 'ch']


import logging


class CustomFormatter(logging.Formatter):
    """Format for log

    """
    grey = '\x1b[38;20m'
    yellow = '\x1b[33;20m'
    blue = '\033[0;34m'
    red = '\x1b[31;20m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'
    format = '%(asctime)s | %(name)s | %(levelname)s |(%(filename)s:%(lineno)d) | %(message)s '

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: blue + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


ch = logging.StreamHandler()

# set global log level
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
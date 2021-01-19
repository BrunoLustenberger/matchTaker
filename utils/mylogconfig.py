"""
Import this module in the "main" file and choose a config
"""

import logging
from logging import handlers


def simplest():
    logging.basicConfig(level=logging.DEBUG)


def simple(filename='log.txt', level=logging.WARNING):
    logging.basicConfig(filename=filename, level=level, filemode='w',
                        format='%(asctime)s | %(levelname)s | %(message)s | %(module)s,%(lineno)d')
    

def standard(filename='log.txt', level=logging.WARNING):
    # see also cookbook, 1st example
    # get the root logger
    rlogger = logging.getLogger()
    # set its level
    rlogger.setLevel(level)
    # create file handler with same level
    fh = logging.FileHandler(filename=filename, mode='a')
    fh.setLevel(level)
    # create console handler for errors and above
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s | %(levelname)s |  %(module)s,%(lineno)d \n %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    rlogger.addHandler(fh)
    rlogger.addHandler(ch)


def standard_rot(filename='log.txt', level=logging.WARNING, max_bytes=16 * 1024, backup_count=5):
    # see also cookbook, 1st example
    # get the root logger
    rlogger = logging.getLogger()
    # set its level
    rlogger.setLevel(level)
    # create file handler with same level
    fh = handlers.RotatingFileHandler(filename, mode='a', maxBytes=max_bytes, backupCount=backup_count)
    fh.setLevel(level)
    # create console handler for errors and above
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s | %(levelname)s |  %(module)s,%(lineno)d \n %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    rlogger.addHandler(fh)
    rlogger.addHandler(ch)

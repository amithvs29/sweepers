import logging
from common import safe_path


def initlogger(filename):
    safe_path(filename)
    logging.basicConfig(filename=filename,
                        filemode='a+',
                        level=logging.DEBUG,
                        format='[%(asctime)s] [%(levelname)8s] --- %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

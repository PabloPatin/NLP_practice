import logging
try:
    from path import ABS_PATH
except ImportError as ex:
    ex.msg = "Please start __init__.py or create path.py with argument ABS_PATH"
    raise ex


DATA_PATH = ABS_PATH + '\\data\\'
LOG_PATH = ABS_PATH + '\\logs\\'
LOG_FILE = 'logger.log'
LOG_LEVEL = logging.INFO
DATA_FILE = 'corpus.dat'
CORPUS_FILE = 'corpus.txt'

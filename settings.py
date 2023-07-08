import logging

try:
    from path import ABS_PATH
except ImportError as ex:
    ex.msg = "Please start __init__.py or create path.py with argument ABS_PATH"
    raise ex

DATA_PATH = ABS_PATH + '\\data\\'
CORPUS_FILE = 'corpus.txt'
DATA_FILE = 'corpus.dat'
DATA_FILE_FORMATS = ['dat']
CORPUS_FILE_FORMATS = ['txt']
FILE_FORMATS = DATA_FILE_FORMATS + CORPUS_FILE_FORMATS

LOG_PATH = ABS_PATH + '\\logs\\'
LOG_FILE = 'logger.log'
LOG_LEVEL = logging.WARNING

TOKEN_DELIMITERS = [' ', '\t', '\n']

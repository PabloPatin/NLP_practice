import logging

from logger import Handler
from classes.meta import TokenMeta


# TODO: create interface
class T9(TokenMeta):
    logger = logging.Logger(name="T9")

    def find_new_words(self, amount):
        pass

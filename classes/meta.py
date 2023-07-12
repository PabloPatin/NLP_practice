import logging
import pickle
from dataclasses import dataclass
from typing import TypeAlias

from classes.logger import Handler
from classes.tokens import Tid, Token, Bigram, Trigram
from settings import DATA_PATH, LOG_LEVEL, DATA_FILE, TOKEN_DELIMITERS

TokenField: TypeAlias = dict[Tid:Token]
BigramField: TypeAlias = dict[Tid:Bigram]
TrigramField: TypeAlias = dict[Tid:Trigram]
TokenCache: TypeAlias = dict[str:Tid]


@dataclass
class MetaInfo:
    token_amount: int
    word_quantity: int
    bigram_amount: int
    trigram_amount: int


class TokenMeta:
    logger = logging.Logger(name="TokenMeta", level=LOG_LEVEL)
    logger.addHandler(Handler)

    def __init__(self):
        self._meta = MetaInfo(
            token_amount=0,
            word_quantity=0,
            bigram_amount=0,
            trigram_amount=0)
        self.bigrams: BigramField = {}
        self.trigrams: TrigramField = {}
        self.token_cache: TokenCache = {}

    def _log_error(self, ex, message):
        self.logger.error(f'{ex.__class__.__name__}: {ex}\n{message}')
        raise ex

    def unpack_file(self, file: str = DATA_FILE) -> None:
        """open {file}.dat and load all tokens, bigrams and trigrams"""
        file_path = DATA_PATH + file
        try:
            with open(file_path, 'rb') as file:
                data = pickle.load(file)
                self._check_the_fields(data, file.name)
                self._meta = data['meta']
                self.token_cache = data['tokens']
                self.bigrams = data['bigrams']
                self.trigrams = data['trigrams']
        except (KeyError, pickle.UnpicklingError, AttributeError) as ex:
            self._log_error(ex, 'The file is corrupted or has an incorrect format, '
                                'please retokenise it, using corpus.txt')
        except EOFError as ex:
            self._log_error(ex, 'The file is empty, please retokenise it, using corpus.txt')
        except FileNotFoundError as ex:
            self._log_error(ex, f'There is no file {file.name} in directory {DATA_PATH}')
        except Exception as ex:
            self._log_error(ex, 'UNKNOWN EXCEPTION')
        else:
            self.logger.info('data loaded successfully')

    def _check_the_fields(self, fields: dict, filename: str) -> None:
        if not all(fields.values()):
            self.logger.warning(f'not all of the data was received from file {filename}')
        for i, j in fields.items():
            if not j:
                self.logger.warning(f'field {i} is empty')

    # @staticmethod
    # def _check_the_field(field: dict) -> tuple[str, bool]:
    #     return field.__name__, bool(field)

    def string_to_tokens(self, text: str) -> list[Tid]:
        """convert string into list of tokens"""
        tokens = []
        boof = ''
        for i in text + ' ':
            if i in TOKEN_DELIMITERS:
                token = self.tid_by_word(boof) if boof in self.token_cache else None
                tokens.append(token)
                boof = ''
            else:
                boof += i
        return tokens

    @staticmethod
    def _sort_dict(data: dict) -> dict:
        def sort_func(x: tuple[Tid:Token]):
            return x[1]

        data = dict(sorted(data.items(), key=sort_func, reverse=True))
        return data

    @staticmethod
    def _max_dict(data: dict) -> tuple:
        return max(data.items(), key=lambda x: x[1].quantity)

    def word_by_tid(self, tid: Tid) -> str:
        return self.bigrams[tid].value

    def tid_by_word(self, word: str) -> Tid:
        return self.token_cache[word]

    def word_sum(self) -> int:
        """return summ of all loaded words"""
        return self._meta.word_quantity

    def token_sum(self):
        """return summ of all loaded tokens"""
        return self._meta.token_amount

    def bigram_sum(self):
        """return summ of all loaded bigrams"""
        return self._meta.bigram_amount

    def trigram_sum(self):
        """return summ of all loaded trigrams"""
        return self._meta.trigram_amount

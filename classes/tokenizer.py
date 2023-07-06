import pickle
import logging
from os.path import exists

from settings import LOG_LEVEL, DATA_PATH
from .logger import Handler
from .meta import TokenMeta
from .tokens import Tid, Bigram, Trigram


class Tokenizer(TokenMeta):
    logger = logging.Logger(name='Tokenizer', level=LOG_LEVEL)
    logger.addHandler(Handler)

    def __init__(self):
        self.cur_tid: Tid = 0
        super().__init__()

    def parse_text(self, text: str) -> None:
        word1, word2, word3 = '', '', ''
        for i in text + ' ':
            if i not in [' ', '\n', '\t']:
                word1 += i
            else:
                self.add_token(word1)
                if word2:
                    self.add_bigram(word2, word1)
                if word3:
                    self.add_trigram(word3, word2, word1)
                word3, word2, word1 = word2, word1, ''

    def add_token(self, token: str) -> None:
        self._meta.word_quantity += 1
        if token not in self.token_cache:
            self._meta.token_amount += 1
            self.token_cache[token] = self.cur_tid
            self.cur_tid += 1

    def add_bigram(self, token1: str, token2: str) -> None:
        token1_id = self.token_cache[token1]
        token2_id = self.token_cache[token2]
        if token1_id in self.bigrams:
            bigram = self.bigrams[token1_id]
            bigram += 1
            if token2_id in bigram.tail:
                bigram.tail[token2_id] += 1
            else:
                self._meta.bigram_amount += 1
                bigram.tail[token2_id] = 1
        else:
            self._meta.bigram_amount += 1
            bigram = Bigram(token1_id, 1, token1, {token2_id: 1})
            self.bigrams[token1_id] = bigram

    def add_trigram(self, token1: str, token2: str, token3: str) -> None:
        token1_id = self.token_cache[token1]
        token2_id = self.token_cache[token2]
        token3_id = self.token_cache[token3]
        head = (token1_id, token2_id)
        if head in self.trigrams:
            trigram = self.trigrams[head]
            trigram += 1
            if token3_id in trigram.tail:
                trigram.tail[token3_id] += 1
            else:
                self._meta.trigram_amount += 1
                trigram.tail[token3_id] = 1
        else:
            self._meta.trigram_amount += 1
            self.trigrams[head] = Trigram(head, 1, f'{token1} {token2}', {token3_id: 1})

    def parse_text_from_file(self, file: str):
        file_path = DATA_PATH + file
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            if not text.split():
                raise EOFError('file is empty')
            self.parse_text(text)
        except EOFError as ex:
            self._log_error(ex, 'The file is empty, please change the corpus.txt file')
        except FileNotFoundError as ex:
            self._log_error(ex, f'There is no file {file.name} in directory {DATA_PATH}')
        except Exception as ex:
            self._log_error(ex, 'UNKNOWN EXCEPTION')
        else:
            self.logger.info(f'{file.name} successfully parsed')

    def pack_file(self, file):
        file_path = DATA_PATH + file
        data = {
            'meta': self._meta,
            'tokens': self.token_cache,
            'bigrams': self.bigrams,
            'trigrams': self.trigrams}
        if not any((self.token_cache, self.bigrams, self.trigrams)):
            self._log_error(ValueError('all of data is empy'),
                            'try to parse or load it from other file first')
        if exists(file_path):
            self.logger.warning(f'file {file} was overwritten')
        with open(file, 'wb') as file:
            pickle.dump(data, file)

    def add_to_file(self, text, file):
        self.unpack_file(file)
        self.parse_text(text)
        self.pack_file(file)

    def word_sum(self):
        return self._meta.word_quantity

    def token_sum(self):
        return self._meta.token_amount

    def bigram_sum(self):
        return self._meta.bigram_amount

    def trigram_sum(self):
        return self._meta.trigram_amount

    def tokens_to_list(self):
        return [i.value for i in self.bigrams.values()]

    def bigrams_to_list(self):
        return [i.value for i in self.trigrams.values()]


if __name__ == '__main__':
    T = Tokenizer()
    T.parse_text_from_file('../data/corpus.txt')
    T.pack_file('../data/corpus.dat')

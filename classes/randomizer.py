import pickle
import logging
from random import choice, randrange

from .logger import Handler
from .meta import TokenMeta
from .tokens import Tid


class Randomizer(TokenMeta):
    def __init__(self, data_file):
        super().__init__()
        self.unpack_file(data_file)
        self.start_tokens: list[Tid] = []
        self.end_tokens: list[Tid] = []
        self._fill_data()
        self.__sentence = ''
        self.__last_word = None
        self.__pre_last_word = None
        self.__temp_len = 0
        self.state = None

    def _fill_data(self):
        end_sign = ['.', '!', '?', '…', '\n']
        for token, bigram in self.bigrams.items():
            if bigram.value.istitle():
                self.start_tokens.append(token)
            if bigram.value[-1] in end_sign:
                self.end_tokens.append(token)

    def generate_sentence(self, min_len=5):
        self.__sentence = ''
        self.__temp_len = 0
        new_word = ''
        while new_word not in self.end_tokens:
            new_word = self.find_next_word(min_len=min_len)
            self.__sentence += self.word_by_tid(new_word) + ' '
        self.__last_word = None
        self.__pre_last_word = None
        return self.__sentence

    def find_next_word(self, last_word='', pre_last_word='', min_len=5):
        word = None
        last = ''
        if not last_word:
            last_word = self.__last_word
        if not pre_last_word:
            pre_last_word = self.__pre_last_word
        if not last_word:
            while word not in self.start_tokens or word in self.end_tokens:
                start_token = choice(self.start_tokens)
                word = start_token
        else:
            bid = last_word
            tail = self.bigrams[bid].tail.copy()
            if pre_last_word:
                tid = pre_last_word
                tail_2 = self.trigrams[(tid, bid)].tail.copy()
                tail = self.__merge_tails(tail, tail_2)
            if self.__temp_len < min_len:
                to_pop = []
                for i in tail.keys():
                    if i in self.end_tokens:
                        to_pop.append(i)
                for i in to_pop[::-1]:
                    last = i
                    tail.pop(i)
            if tail:
                word = self.__choice(tail)
            else:
                word = last
        word = word
        self.__pre_last_word = self.__last_word
        self.__last_word = word
        self.__temp_len += 1
        return word

    @staticmethod
    def __choice(tail) -> Tid:
        tid = 0
        count = 0
        tail_ranges = []
        for i, j in tail.items():
            tail_ranges.append(range(count, j + count))
            count += j
        rand = randrange(count)
        for i, j in enumerate(tail_ranges):
            if rand in j:
                tid = i
                break
        tid = tuple(tail.keys())[tid]
        return tid

    @staticmethod
    def __merge_tails(tail_1, tail_2):
        for k, v in tail_1.items():
            if k in tail_2:
                tail_2[k] += v
            else:
                tail_2[k] = v
        return tail_2

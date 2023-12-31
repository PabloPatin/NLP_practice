import logging
from random import choice, randrange

from classes.logger import Handler
from classes.meta import TokenMeta
from classes.tokens import Tid
from settings import LOG_LEVEL, DATA_FILE


class Randomizer(TokenMeta):
    logger = logging.Logger(name='Randomizer', level=LOG_LEVEL)
    logger.addHandler(Handler)

    def __init__(self):
        super().__init__()
        self.start_tokens: list[Tid] = []
        self.end_tokens: list[Tid] = []
        self.__sentence = ''
        self.__last_word = None
        self.__pre_last_word = None
        self.__temp_len = 0

    def unpack_file(self, file: str = DATA_FILE) -> None:
        super().unpack_file(file)
        self._fill_data()

    def _fill_data(self):
        end_sign = ['.', '!', '?', '…', '\n']
        for token, bigram in self.bigrams.items():
            if bigram.value.istitle():
                self.start_tokens.append(token)
            if bigram.value[-1] in end_sign:
                self.end_tokens.append(token)

    def generate_sentence(self, min_len=5):
        sentence, new_word = '', ''
        while new_word not in self.end_tokens:
            new_word = self._find_next_word(min_len=min_len)
            sentence += self.word_by_tid(new_word) + ' '
        self.reset_generator()
        return sentence

    def reset_generator(self):
        self.__last_word = ''
        self.__pre_last_word = ''
        self.__temp_len = 0

    def __pop_end_tokens_from_tail(self, tail: dict[Tid, int]) -> dict[Tid, int]:
        to_pop = []
        last = None
        for i in tail.keys():
            if i in self.end_tokens:
                to_pop.append(i)
        for i in to_pop[::-1]:
            last = i
            tail.pop(i)
        if not tail:
            if not last:
                self.logger.debug('no one word matched')
                last = choice(self.start_tokens)
            tail = {last: 1}
        return tail

    def _find_next_word(self, min_len=5):
        word = None
        last_word = self.__last_word
        pre_last_word = self.__pre_last_word
        if not last_word:
            while word not in self.start_tokens or word in self.end_tokens:
                start_token = choice(self.start_tokens)
                word = start_token
        else:
            bid = last_word
            tail = self.bigrams[bid].tail.copy()
            if pre_last_word:
                trid = pre_last_word
                tail_2 = self.trigrams[(trid, bid)].tail.copy()
                tail = self.__merge_tails(tail, tail_2)
            if self.__temp_len < min_len:
                tail = self.__pop_end_tokens_from_tail(tail)
            word = self.__choice(tail)
        self.__update_temp(word)
        return word

    def __update_temp(self, word):
        self.__pre_last_word = self.__last_word
        self.__last_word = word
        self.__temp_len += 1

    def find_next_word(self):
        """find next word for sentence"""
        return self.word_by_tid(self._find_next_word())

    @staticmethod
    def __choice(tail: dict[Tid, int]) -> Tid:
        """choose random word from tail"""
        tid, count = 0, 0
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


if __name__ == "__main__":
    R = Randomizer()
    R.unpack_file()
    for _ in range(15):
        print(R.find_next_word(), end=' ')
    print('\n'+R.generate_sentence())


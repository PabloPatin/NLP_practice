import pickle
from dataclasses import dataclass, asdict
from functools import total_ordering
from random import choice, randrange

Tid = int


@total_ordering
@dataclass
class Token:
    tid: Tid
    quantity: int
    value: str

    def __eq__(self, other):
        return self.quantity == other.quantity

    def __lt__(self, other):
        return self.quantity < other.quantity

    def __add__(self, other: int):
        self.quantity += 1
        return self


@dataclass
class Bigram(Token):
    tail: dict[Tid:int]


@dataclass
class Trigram(Bigram):
    tid: tuple[Tid, Tid]


TokenField = dict[Tid:Token]
TokenCache = dict[str:Tid]


@dataclass
class MetaInfo:
    token_amount: int
    word_quantity: int
    bigram_amount: int
    trigram_amount: int


class TokenMeta:
    def __init__(self):
        self._meta = MetaInfo(
            token_amount=0,
            word_quantity=0,
            bigram_amount=0,
            trigram_amount=0)
        self.bigrams: TokenField = {}
        self.trigrams: TokenField = {}
        self.token_cache: TokenCache = {}

    def unpack_file(self, file):
        with open(file, 'rb') as file:
            data = pickle.load(file)
            self._meta = data['meta']
            self.token_cache = data['tokens']
            self.bigrams = data['bigrams']
            self.trigrams = data['trigrams']

    def string_to_tokens(self, text) -> list[Tid]:
        tokens = []
        boof = ''
        for i in text:
            if i in [' ', '\n', '\t']:
                if boof in self.token_cache:
                    tokens.append(self.token_cache[boof])
                else:
                    tokens.append(None)
                boof = ''
            else:
                boof += i
        if boof in self.token_cache:
            tokens.append(self.token_cache[boof])
        else:
            tokens.append(None)
        return tokens

    @staticmethod
    def _sort_dict(data: dict):
        def sort_func(x: tuple[Tid:Token]):
            return x[1]

        data = dict(sorted(data.items(), key=sort_func, reverse=True))
        return data

    @staticmethod
    def _max_dict(data: dict) -> tuple:
        return max(data.items(), key=lambda x: x[1].quantity)

    def word_by_tid(self, tid: Tid):
        return self.bigrams[tid].value


class Tokenizer(TokenMeta):
    def __init__(self):
        self.cur_tid: Tid = 0
        super().__init__()

    def parse_text(self, text: str):
        word1, word2, word3 = '', '', ''
        for i in text:
            if i not in [' ', '\n', '\t']:
                word1 += i
            else:
                self.add_token(word1)
                if word2:
                    self.add_bigram(word2, word1)
                if word3:
                    self.add_trigram(word3, word2, word1)
                word3, word2, word1 = word2, word1, ''
        self.add_token(word2)
        if word1:
            self.add_token(word1)

    def add_token(self, token: str):
        self._meta.word_quantity += 1
        if token not in self.token_cache:
            self._meta.token_amount += 1
            self.token_cache[token] = self.cur_tid
            self.cur_tid += 1

    def add_bigram(self, token1: str, token2: str):
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

    def add_trigram(self, token1: str, token2: str, token3: str):
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
        with open(file, 'r', encoding='utf-8') as file:
            text = file.read()
            self.parse_text(text)

    def pack_file(self, file):
        data = {
            'meta': asdict(self._meta),
            'tokens': self.token_cache,
            'bigrams': self.bigrams,
            'trigrams': self.trigrams}
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


class Randomizer(TokenMeta):
    def __init__(self, data_path):
        super().__init__()
        self.unpack_file(data_path)
        self.start_tokens: list[Tid] = []
        self.end_tokens: list[Tid] = []
        self.stend_tokens: list[Tid] = []
        self._fill_data()
        self.__sentence = ''
        self.__last_word = None
        self.__pre_last_word = None
        self.__temp_len = 0
        self.state = None

    def _fill_data(self):
        endsign = ['.', '!', '?', '…', '\n']
        for token, bigram in self.bigrams.items():
            if bigram.value.istitle() and bigram.value[-1] in endsign:
                self.stend_tokens.append(token)
            if bigram.value.istitle():
                self.start_tokens.append(token)
            if bigram.value[-1] in endsign:
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
                topop = []
                for i in tail.keys():
                    if i in self.end_tokens:
                        topop.append(i)
                for i in topop[::-1]:
                    last = i
                    tail.pop(i)
            if tail:
                word = self.__choise(tail)
            else:
                word = last
        word = word
        self.__pre_last_word = self.__last_word
        self.__last_word = word
        self.__temp_len += 1
        return word

    @staticmethod
    def __choise(tail) -> Tid:
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


if __name__ == "__main__":
    T = Tokenizer()
    T.parse_text_from_file('corpus.txt')
    # T.unpack_file('corpus.dat')
    print(T.trigrams)
    # print(T.string_to_tokens('I am cold'))
    T.pack_file('corpus.dat')
    print(T.token_sum())

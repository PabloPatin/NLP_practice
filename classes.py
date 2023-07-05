import json
from dataclasses import dataclass, asdict
from functools import total_ordering

Tid = int


@total_ordering
@dataclass
class Token:
    tid: Tid
    quantity: int
    val: str

    def __eq__(self, other):
        return self.quantity == other.quantity

    def __lt__(self, other):
        return self.quantity < other.quantity

    def __add__(self, other: int):
        self.quantity += 1
        return self


@total_ordering
@dataclass
class Bigram:
    bid: Tid
    quantity: int
    head: Tid
    tail: dict[Tid:int]

    def __eq__(self, other):
        return self.quantity == other.quantity

    def __lt__(self, other):
        return self.quantity < other.quantity

    def __add__(self, other: int):
        self.quantity += 1
        return self


@total_ordering
@dataclass
class Trigram:
    trid: Tid
    quantity: int
    head: tuple[Tid, Tid]
    tail: dict[Tid:int]

    def __eq__(self, other):
        return self.quantity == other.quantity

    def __lt__(self, other):
        return self.quantity < other.quantity

    def __add__(self, other: int):
        self.quantity += 1
        return self


TokenField = dict[Tid:Token]
TokenCache = dict[str:Tid]


class TokenMeta:
    def __init__(self):
        self._meta = {
            'token_amount': 0,
            'word_quantity': 0,
            'bigram_quantity': 0,
            'unique_bigram_amount': 0,
            'trigram_quantity': 0,
            'unique_trigram_amount': 0,
            'trigrams': True
        }
        self.tokens: TokenField = {}
        self.bigrams: TokenField = {}
        self.trigrams: TokenField = {}
        self.token_cache: TokenCache = {}
        self.bigram_cache: TokenCache = {}
        self.trigram_cache: TokenCache = {}

    def from_json(self, file):
        with open(file, 'r', encoding='utf-8') as file:
            self._meta, *args = json.load(file).values()
            if self._meta['trigrams']:
                self.tokens, self.bigrams, self.trigrams = args
            else:
                self.tokens, self.bigrams = args
            self.tokens = {i['tid']: Token(**i) for i in self.tokens}
            self.bigrams = {i['bid']: Bigram(**i) for i in self.bigrams}
            self.trigrams = {i['trid']: Trigram(**i) for i in self.trigrams}

    def set_cache(self):
        for token in self.tokens.values():
            self.token_cache[token.val] = token.tid
        for bigram in self.bigrams.values():
            self.token_cache[bigram.head] = bigram.bid
        for trigram in self.trigrams.values():
            self.token_cache[trigram.head] = trigram.trid

    def string_to_tokens(self, text) -> list[Tid]:
        self.set_cache()
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


class Tokenizer(TokenMeta):
    def __init__(self):
        self.cur_tid: Tid = 0
        self.cur_bid: Tid = 0
        self.cur_trid: Tid = 0
        super().__init__()

    def __sort(self):
        def sort_func(x: tuple[Tid:Token]):
            return x[1]

        self.tokens = dict(sorted(self.tokens.items(), key=sort_func, reverse=True))
        self.bigrams = dict(sorted(self.bigrams.items(), key=sort_func, reverse=True))
        self.trigrams = dict(sorted(self.trigrams.items(), key=sort_func, reverse=True))

    def parse_text(self, text: str):
        word1 = ''
        word2 = ''
        word3 = ''
        for i in text:
            if i not in [' ', '\n', '\t']:
                word1 += i
            else:
                self.add_token(word1)
                if word2:
                    self.add_bigram(word2, word1)
                if word3:
                    self.add_trigram(word3, word2, word1)
                word3 = word2
                word2 = word1
                word1 = ''
        if word1 != '':
            self.add_token(word1)
        self.__sort()

    def add_token(self, token: str):
        self._meta['word_quantity'] += 1
        if token in self.token_cache:
            tid = self.token_cache[token]
            self.tokens[tid] += 1
        else:
            self._meta['token_amount'] += 1
            self.token_cache[token] = self.cur_tid
            self.tokens[self.cur_tid] = Token(self.cur_tid, 1, token)
            self.cur_tid += 1

    def add_bigram(self, token1: str, token2: str):
        self._meta['bigram_quantity'] += 1
        token1_id = self.token_cache[token1]
        token2_id = self.token_cache[token2]
        head = token1_id,
        if head in self.bigram_cache:
            bid = self.bigram_cache[head]
            bigram = self.bigrams[bid]
            self.bigrams[bid].quantity += 1
            if token2_id in bigram.tail:
                bigram.tail[token2_id] += 1
            else:
                self._meta['unique_bigram_amount'] += 1
                bigram.tail[token2_id] = 1
        else:
            self._meta['unique_bigram_amount'] += 1
            self.bigram_cache[head] = self.cur_bid
            self.bigrams[self.cur_bid] = Bigram(self.cur_bid, 1, token1_id, {token2_id: 1})
            self.cur_bid += 1

    def add_trigram(self, token1: str, token2: str, token3: str):
        self._meta['trigram_quantity'] += 1
        token1_id = self.token_cache[token1]
        token2_id = self.token_cache[token2]
        token3_id = self.token_cache[token3]
        head = (token1_id, token2_id)
        if head in self.trigram_cache:
            trid = self.trigram_cache[head]
            trigram = self.trigrams[trid]
            self.trigrams[trid].quantity += 1
            if token3_id in trigram.tail:
                trigram.tail[token3_id] += 1
            else:
                self._meta['unique_trigram_amount'] += 1
                trigram.tail[token3_id] = 1
        else:
            self._meta['unique_trigram_amount'] += 1
            self.trigram_cache[head] = self.cur_trid
            self.trigrams[self.cur_trid] = Trigram(self.cur_trid, 1, token1_id, {token3_id: 1})
            self.cur_trid += 1

    def parse_text_from_file(self, file: str):
        with open(file, 'r', encoding='utf-8') as file:
            text = file.read()
            self.parse_text(text)

    @staticmethod
    def __convert_to_json(data: dict[int:Token]):
        return list(map(asdict, data.values()))

    def to_json(self, file):
        with open(file, 'w', encoding='utf-8') as file:
            data = {
                'meta': self._meta,
                'tokens': self.__convert_to_json(self.tokens),
                'bigrams': self.__convert_to_json(self.bigrams),
                'trigrams': self.__convert_to_json(self.trigrams)}
            json.dump(data, file, indent=4, ensure_ascii=False)

    def add_to_json(self, text, file):
        self.from_json(file)
        self.parse_text(text)
        self.to_json(file)

    def from_json(self, file):
        super().from_json(file)
        super().set_cache()

    def word_sum(self):
        return self._meta['word_quantity']

    def token_sum(self):
        return self._meta['token_amount']

    def bigram_sum(self):
        return self._meta['bigram_quantity']

    def unique_bigram_sum(self):
        return self._meta['unique_bigram_amount']

    def tokens_to_list(self):
        return [i.val for i in self.tokens.values()]

    def bigrams_to_list(self):
        return [' '.join(i.head) for i in self.trigrams]


class Randomizer:
    def __init__(self, json_path, **params):
        pass


if __name__ == "__main__":
    T = Tokenizer()
    T.parse_text_from_file('corpus.txt')
    # T.from_json('corpus.json')
    print(T.string_to_tokens('I am cold'))
    T.to_json('corpus.json')
    print(T.bigram_sum())

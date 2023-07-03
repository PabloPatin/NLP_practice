import json
class Tokenizer:
    def __init__(self):
        self.tokens: dict = {}
        self.__token_amount = None
        self.__word_amount = None

    def __sort(self):
        self.tokens = dict(sorted(self.tokens.items(), key=lambda x: x[1], reverse=True))

    def add_to_json(self, text, file):
        self.from_json(file)
        self.parse_text(text)
        self.to_json(file)

    def parse_text(self, text: str) -> dict:
        boof = ''
        for i in text:
            if i not in [' ', '\n', '\t']:
                boof += i
            else:
                self.add_token(boof)
                boof = ''
        if boof != '':
            self.add_token(boof)
        self.__sort()
        return self.tokens

    def parse_text_from_file(self, file: str) -> dict:
        with open(file, 'r', encoding='utf-8') as file:
            text = file.read()
        return self.parse_text(text)

    def add_token(self, st):
        if st in self.tokens.keys():
            self.tokens[st] += 1
        else:
            self.tokens[st] = 1

    def to_json(self, file):
        with open(file, 'w', encoding='utf-8') as file:
            json.dump(self.tokens, file, indent=4, ensure_ascii=False)

    def from_json(self, file):
        with open(file, 'r', encoding='utf-8') as file:
            self.tokens = json.load(file)
        return self.tokens

    def word_sum(self):
        self.__word_amount = sum(self.tokens.values())
        return self.__word_amount

    def token_sum(self):
        self.__token_amount = len(self.tokens.keys())
        return self.__token_amount


def s(x):
    print(Tokenizer.tokens[x])
    return Tokenizer.tokens[x]


if __name__ == "__main__":
    T = Tokenizer()
    T.parse_text_from_file('corpus.txt')
    print(T.word_sum())
    print(T.token_sum())
    print(T.tokens)
    T.to_json('corpus.json')

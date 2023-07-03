from classes import Tokenizer

if __name__ == '__main__':
    T = Tokenizer()
    T.from_json('corpus.json')
    print(T.tokens)
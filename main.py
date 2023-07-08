from classes import Tokenizer, Randomizer


if __name__ == '__main__':
    T = Tokenizer()
    T.unpack_file()
    print(T.word_sum(), T.token_sum(), T.bigram_sum(), T.trigram_sum())
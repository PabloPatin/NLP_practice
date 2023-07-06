from classes import Tokenizer, Randomizer


if __name__ == '__main__':
    T = Tokenizer()
    T.unpack_file('corpus.dat')
    R = Randomizer('corpus.dat')
    print(R.generate_sentence(min_len=80))
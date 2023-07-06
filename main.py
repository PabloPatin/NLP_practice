from classes import *
import pickle


class A:
    a = 5
    b = 6

    def __init__(self):
        self.c = {self.a: self.b}

    def __repr__(self):
        return f'{self.a=}, {self.b=}, {self.c=}'


if __name__ == '__main__':
    with open('corpus.dat', 'wb') as file:
        pickle.dump(A(), file)

    with open('corpus.dat', 'rb') as file:
        a = pickle.load(file)
    print(a)

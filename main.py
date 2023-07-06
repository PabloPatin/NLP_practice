import pickle

if __name__ == '__main__':
    with open('corpus.dat', 'wb') as file:
        pickle.dump({'meta': {1:2, 2:3}}, file)

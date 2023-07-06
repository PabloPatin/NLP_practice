from classes import *
import os


class FileFormatError(Exception):
    pass


class Datafile:
    def __init__(self, path):
        if os.path.exists(path):
            self.format = path.split('.')[-1]
            if self.format in ['dat', 'txt']:
                self.path = path
            else:
                raise FileFormatError('Не верный формат файла, ожидается .txt или .dat')
        else:
            raise FileNotFoundError('Не верный путь файла')


class Interface:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Interface, cls).__new__(cls)
        return cls.__instance

    @staticmethod
    def __input(massage=''):
        res = input(f'{massage}\n> ')
        return res

    @staticmethod
    def __datafile_validate(path):
        try:
            datafile = Datafile(path)
        except (FileFormatError, FileNotFoundError) as ex:
            print(ex)
            return None
        else:
            return datafile

    def execute_command(self, inp):
        pass

    def print_statistic(self):
        print('Статистика корпуса текста')
        print(f'Всего токенов: {self.tk.word_sum()}')
        print(f'Уникальных токенов: {self.tk.token_sum()}')
        print(f'Всего биграмм: {self.tk.bigram_sum()}')
        print(f'Уникальных биграмм: {self.tk.trigram_sum()}')

    def __init__(self):
        self.tk = Tokenizer()
        datafile = None
        while not datafile:
            path = self.__input('Введите путь к файлу с корпусом')
            datafile = self.__datafile_validate(path)
        if datafile.format == 'dat':
            self.tk.unpack_file(datafile.path)
        elif datafile.format == 'txt':
            self.tk.parse_text_from_file(datafile.path)
        self.print_statistic()

        inp = self.__input()
        while inp != 'exit':
            self.execute_command(inp)
            inp = self.__input()
        exit()


class TokenInterface(Interface):
    def print_statistic(self):
        print('Статистика корпуса текста')
        print(f'Всего токенов: {self.tk.word_sum()}')
        print(f'Уникальных токенов: {self.tk.token_sum()}')

    def execute_command(self, inp):
        try:
            if inp.isnumeric():
                inp = int(inp)
                print(self.tk.bigrams[inp].value)
            else:
                print(self.tk.token_cache[inp])
        except ValueError:
            print('ValueError. Введите числовое значение')
        except IndexError:
            print('IndexError. Ввведите число из диапазона токенов')
        except KeyError:
            print('KeyError. Введена несуществующий токен')


class BigramInterface(Interface):
    def print_statistic(self):
        print('Статистика корпуса текста')
        print(f'Всего биграмм: {self.tk.word_sum() - 1}')
        print(f'Уникальных биграмм: {self.tk.bigram_sum()}')

    def execute_command(self, inp):
        inp = tuple(inp.split())
        try:
            if len(inp) == 2:
                token1, token2 = inp
                if token1.isnumeric() and token2.isnumeric():
                    token1, token2 = self.tk.word_by_tid(int(token1)), self.tk.word_by_tid(int(token2))
                else:
                    token1, token2 = self.tk.token_cache[token1], self.tk.token_cache[token2]
                print(token1, token2)
            elif len(inp) == 1:
                tid = self.tk.token_cache[inp[0]]
                bigram = self.tk.bigrams[tid]
                print(f'Head: {bigram.value}')
                for tail, count in bigram.tail.items():
                    print(f'Tail: {self.tk.word_by_tid(int(tail))}\tCount: {count}')
            else:
                print('Неверное число аргументов: введите 1 или 2 аргумента')
        except ValueError:
            print('ValueError. Введите два слова через запятую')
        except IndexError:
            print('IndexError. Ввведите числа из диапазона токенов')
        except KeyError:
            print('Такой биграммы не существует')


if __name__ == '__main__':
    # T = Tokenizer()
    # BigramInterface()
    R = Randomizer('corpus.dat')
    for i in range(10):
        print(R.generate_sentence())

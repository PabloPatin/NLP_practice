from classes import *
import os

from settings import DATA_PATH, FILE_FORMATS, DATA_FILE_FORMATS, CORPUS_FILE_FORMATS, TOKEN_DELIMITERS


class FileFormatError(Exception):
    pass


class Datafile:
    def __init__(self, file):
        self.path = DATA_PATH + file
        self.name = file
        self.format = file.split('.')[-1]
        self._check_if_exist()

    def _check_if_exist(self):
        if os.path.exists(self.path):
            if self.format not in FILE_FORMATS:
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
    def __decorated_input(massage=''):
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
        """print statistics of file"""
        print('Статистика корпуса текста')
        print(f'Всего токенов: {self.tk.word_sum()}')
        print(f'Уникальных токенов: {self.tk.token_sum()}')
        print(f'Всего биграмм: {self.tk.bigram_sum()}')
        print(f'Уникальных биграмм: {self.tk.trigram_sum()}')

    def __init__(self):
        self.tk = Tokenizer()
        datafile = None
        while not datafile:
            file = self.__decorated_input('Введите имя файла с корпусом')
            datafile = self.__datafile_validate(file)
        if datafile.format in DATA_FILE_FORMATS:
            self.tk.unpack_file(datafile.name)
        elif datafile.format in CORPUS_FILE_FORMATS:
            self.tk.parse_text_from_file(datafile.name)
        self.print_statistic()

        inp = self.__decorated_input()
        while inp != 'exit':
            self.execute_command(inp)
            inp = self.__decorated_input()
        exit()


class TokenInterface(Interface):
    def print_statistic(self):
        print('Статистика корпуса текста')
        print(f'Всего токенов: {self.tk.word_sum()}')
        print(f'Уникальных токенов: {self.tk.token_sum()}')

    @staticmethod
    def _catch_exception(func):
        def wrapper(self, inp):
            try:
                func(self, inp)
            except AssertionError as ex:
                print(f'AssertionError {ex}')
            except IndexError:
                print('IndexError. Ввведите число из диапазона токенов')
            except KeyError:
                print('KeyError. Введен несуществующий токен')

        return wrapper

    @_catch_exception
    def execute_command(self, inp):
        if inp.isnumeric():
            inp = int(inp)
            print(self.tk.bigrams[inp].value)
        elif any(map(lambda x: x in inp, TOKEN_DELIMITERS)):
            raise AssertionError('Введите число или токен без разделителей')
        else:
            print(self.tk.token_cache[inp])


class BigramInterface(Interface):
    def print_statistic(self):
        print('Статистика корпуса текста')
        print(f'Всего биграмм: {self.tk.word_sum() - 1}')
        print(f'Уникальных биграмм: {self.tk.bigram_sum()}')

    @staticmethod
    def _catch_exception(func):
        def wrapper(self, inp):
            try:
                func(self, inp)
            except AssertionError as ex:
                print(f'AssertionError {ex}')
            except ValueError:
                print('ValueError. Введите два слова через запятую')
            except IndexError:
                print('IndexError. Ввведите числа из диапазона токенов')
            except KeyError:
                print('Такой биграммы не существует')

        return wrapper

    @_catch_exception
    def execute_command(self, inp):
        inp = tuple(inp.split())
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
            raise AssertionError('Неверное число аргументов: введите 1 или 2 аргумента')


if __name__ == '__main__':
    TokenInterface()
    BigramInterface()

from classes import Tokenizer
import os


class FileFormatError(Exception):
    pass


class Datafile:
    def __init__(self, path):
        if os.path.exists(path):
            self.format = path.split('.')[-1]
            if self.format in ['json', 'txt']:
                self.path = path
            else:
                raise FileFormatError('Не верный формат файла, ожидается .txt или .json')
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
        print(f'Уникальных биграмм: {self.tk.unique_bigram_sum()}')

    def __init__(self):
        self.tk = Tokenizer()
        datafile = None
        while not datafile:
            path = self.__input('Введите путь к файлу с корпусом')
            datafile = self.__datafile_validate(path)
        if datafile.format == 'json':
            self.tk.from_json(datafile.path)
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
        token_list = self.tk.tokens_key_to_list()
        try:
            if inp.isnumeric():
                inp = int(inp)
                print(token_list[inp])
            else:
                print(self.tk.tokens[inp])
        except ValueError:
            print('ValueError. Введите числовое значение')
        except IndexError:
            print('IndexError. Ввведите число из диапазона токенов')
        except KeyError:
            print('KeyError. Введена несуществующий токен')


class BigramInterface(Interface):
    def print_statistic(self):
        print('Статистика корпуса текста')
        print(f'Всего биграмм: {self.tk.bigram_sum()}')
        print(f'Уникальных биграмм: {self.tk.unique_bigram_sum()}')

    def execute_command(self, inp):
        bigram_list = self.tk.bigrams_key_to_list()
        try:
            if inp.isnumeric():
                inp = int(inp)
                print(f'Голова: {bigram_list[inp][0]}\tХвост: {bigram_list[inp][1]}')
            else:
                print(self.tk.bigrams[tuple(inp.split())])
        except ValueError:
            print('ValueError. Введите числовое значение')
        except IndexError:
            print('IndexError. Ввведите число из диапазона токенов')
        except KeyError:
            print('KeyError. Введена несуществующая биграмма')


if __name__ == '__main__':
    T = Tokenizer()
    BigramInterface()

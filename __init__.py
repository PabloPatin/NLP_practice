import os

path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '\\\\')
print(path)
with open(f'{path}\\path.py', 'w', encoding='utf-8') as file:
    file.write(f"ABS_PATH = '{path}'")
    print('lol')

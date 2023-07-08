import os

with open('path.py', 'w', encoding='utf-8') as file:
    file.write(f"ABS_PATH = '{os.path.dirname(os.path.abspath(__file__))}'")

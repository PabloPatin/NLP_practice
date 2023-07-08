import os

with open('path.py', 'w', encoding='utf-8') as file:
    file.write(f"PATH = '{os.path.dirname(os.path.abspath(__file__))}'")

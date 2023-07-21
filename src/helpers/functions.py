'''./src/helpers/functions.py'''

from typing import Callable


col_to_int: Callable[[str], int] = lambda col: ord(col) - 97

int_to_col: Callable[[int], str] = lambda num: chr(num + 97)

import os
from typing import Callable


def clear() -> int:
    status: int = os.system('cls') if os.name == 'nt' else os.system('clear')
    print('\n\t ---- Welcome to the Chess game! ---- \n')
    return status
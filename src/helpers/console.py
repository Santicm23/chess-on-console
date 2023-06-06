
import os


def clear() -> int:
    status: int = os.system('cls') if os.name == 'nt' else os.system('clear')
    print('\n\t ---- Welcome to the Chess game! ---- \n')
    return status

def clear_playing(msg = 'chess') -> int:
    status: int = os.system('cls') if os.name == 'nt' else os.system('clear')
    print(f'\n\t ---- Playing {msg}! ---- \n')
    return status
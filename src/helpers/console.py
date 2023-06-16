
import os
from typing import Sequence

import questionary


def clear() -> int:
    status: int = os.system('cls') if os.name == 'nt' else os.system('clear')
    print('\n\t ---- Welcome to the Chess game! ---- \n')
    return status

def clear_playing(msg: str = 'chess') -> int:
    status: int = os.system('cls') if os.name == 'nt' else os.system('clear')
    print(f'\n\t ---- Playing {msg}! ---- \n')
    return status

def get_text_input(question: str) -> str:
    return questionary.text(question).ask()

def get_list_input(question: str, choices: Sequence[str]) -> str:
    return questionary.select(question,
            choices = choices,
        ).ask()

def get_choices_input(question: str, choices: Sequence[str]) -> str:
    return questionary.checkbox(question,
            choices = choices,
        ).ask()



import os
from typing import Iterable

import inquirer


def clear() -> int:
    status: int = os.system('cls') if os.name == 'nt' else os.system('clear')
    print('\n\t ---- Welcome to the Chess game! ---- \n')
    return status

def clear_playing(msg: str = 'chess') -> int:
    status: int = os.system('cls') if os.name == 'nt' else os.system('clear')
    print(f'\n\t ---- Playing {msg}! ---- \n')
    return status

def get_text_input(question: str) -> str:
    questions = [
        inquirer.Text('input',
                message = question,
            ),
        ]
    answer = inquirer.prompt(questions)

    assert answer is not None

    return answer['input']

def get_list_input(question: str, choices: Iterable[str]) -> str:
    questions = [
        inquirer.List('input',
                message = question,
                choices = choices,
            ),
        ]
    answer = inquirer.prompt(questions)

    assert answer is not None

    return answer['input']


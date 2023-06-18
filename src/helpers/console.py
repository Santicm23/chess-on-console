
import os
from typing import Sequence

import questionary
Choice = questionary.Choice

from ..models.game import Game, GameOver


principal_style = 'fg:#673ab7 bold'
secondary_style = 'fg:#3c9be9 bold'

style = questionary.Style([
    ('qmark', principal_style),          # token in front of the question
    ('question', 'bold'),               # question text
    ('answer', secondary_style),        # submitted answer text behind the question
    ('pointer', principal_style),        # pointer used in select and checkbox prompts
    ('highlighted', principal_style),    # pointed-at choice in select and checkbox prompts
    ('selected', secondary_style),      # style for a selected item of a checkbox
])

print_prettier = questionary.print

def clear() -> int:
    status: int = os.system('cls') if os.name == 'nt' else os.system('clear')
    print_prettier('\n\t ---- Welcome to the Chess game! ---- \n', style=principal_style)
    return status

def clear_playing(msg: str = 'chess') -> int:
    status: int = os.system('cls') if os.name == 'nt' else os.system('clear')
    print_prettier(f'\n\t ---- Playing ', style=principal_style, end='')
    print_prettier(msg, style=secondary_style, end='')
    print_prettier('! ---- \n', style=principal_style)
    return status

def get_text_input(question: str) -> str:
    return questionary.text(question,
            style = style
        ).ask()

def get_list_input(question: str, choices: Sequence[str]) -> str:
    return questionary.select(question,
            choices = choices,
            style = style
        ).ask()

def get_choices_input(question: str, choices: Sequence[str], default_choices: list[str] = []) -> list[str]:
    list_choices: list[Choice] = list(map(lambda choice: questionary.Choice(choice, checked = choice in default_choices), choices))
    return questionary.checkbox(question,
            choices = list_choices,
            style = style
        ).ask()

def print_turn(turn: str) -> None:
    print_prettier('\nTurn: ', style=principal_style, end='')
    print_prettier(turn, style='bold', end='')
    print_prettier(' to move\n', style=principal_style)

def print_game(game: Game) -> None:
    print_prettier(str(game), style='bold')
    print_prettier(repr(game), style='fg:grey')

def print_game_over(game: Game, game_over: GameOver) -> None:

    clear_playing()

    print_game(game)

    print_prettier('\nGame Over!', style=principal_style, end='\n\n')

    print_prettier(game_over.score, style=secondary_style, end=' ')
    if game_over.winner:
        print_prettier(f'{game_over.winner.name.lower()} wins! by', style='bold', end=' ')
    else:
        print_prettier('It is a Draw! by', style='bold', end=' ')
    print_prettier(game_over.game_over_status.name.lower(), style='bold italic fg:grey', end='\n\n')

    get_text_input('Press enter to continue')


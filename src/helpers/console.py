
import os
from typing import Sequence, Optional

import questionary

from src.models.game import Game, GameOver


Choice = questionary.Choice

PRINCIPAL_STYLE = 'fg:#673ab7 bold'
SECONDARY_STYLE = 'fg:#3c9be9 bold'

style = questionary.Style([
    ('qmark', PRINCIPAL_STYLE),         # token in front of the question
    ('question', 'bold'),               # question text
    ('answer', SECONDARY_STYLE),        # submitted answer text behind the question
    ('pointer', PRINCIPAL_STYLE),       # pointer used in select and checkbox prompts
    ('highlighted', PRINCIPAL_STYLE),   # pointed-at choice in select and checkbox prompts
    ('selected', SECONDARY_STYLE),      # style for a selected item of a checkbox
])

print_prettier = questionary.print

def clear() -> int:
    '''
    Clears the console and prints a default message.

    Returns
    -------
    `int`
        The status of the command.
    '''

    status: int = os.system('cls') if os.name == 'nt' else os.system('clear')
    print_prettier('\n\t ---- Welcome to the Chess game! ---- \n', style=PRINCIPAL_STYLE)
    return status

def clear_playing(msg: str = 'chess') -> int:
    '''
    Clears the console and prints a message for playing.

    Parameters
    ----------
    `commands : dict[str, Callable[[], None]]`
        A dictionary of commands that the user can execute.
    
    Returns
    -------
    `int`
        The status of the command.
    '''

    status: int = os.system('cls') if os.name == 'nt' else os.system('clear')
    print_prettier('\n\t ---- Playing ', style=PRINCIPAL_STYLE, end='')
    print_prettier(msg, style=SECONDARY_STYLE, end='')
    print_prettier('! ---- \n', style=PRINCIPAL_STYLE)
    return status

def get_text_input(question: str) -> str:
    '''
    Asks the user to enter a text.
    
    Parameters
    ----------
    `question : str`
        The question to ask the user.

    Returns
    -------
    `str`
        The text entered by the user.
    '''
    return questionary.text(question,
            style = style
        ).ask()

def get_list_input(question: str, choices: Sequence[str]) -> str:
    '''
    Asks the user to select a choice from a list of choices.

    Parameters
    ----------
    `question : str`
        The question to ask the user.
    `choices : Sequence[str]`
        The list of choices.

    Returns
    -------
    `str`
        The choice selected by the user.
    '''

    return questionary.select(question,
            choices = choices,
            style = style
        ).ask()

def get_choices_input(
        question: str,
        choices: Sequence[str],
        default_choices: Optional[list[str]]
) -> list[str]:
    '''
    Asks the user to select one or more choices from a list of choices.

    Parameters
    ----------
    `question : str`
        The question to ask the user.
    `choices : Sequence[str]`
        The list of choices.
    `default_choices : Optional[list[str]]`
        The default choices.

    Returns
    -------
    `list[str]`
        The list of choices selected by the user.
    '''

    if default_choices is None:
        default_choices = []

    list_choices: list[Choice] = list(map(
        lambda choice: questionary.Choice(choice, checked = choice in default_choices),
        choices
    ))
    return questionary.checkbox(question,
            choices = list_choices,
            style = style
        ).ask()

def print_turn(turn: str) -> None:
    '''
    Prints the turn of the player to move.

    Parameters
    ----------
    `turn : str`
        The turn of the player to move.
    '''

    print_prettier('\nTurn: ', style=PRINCIPAL_STYLE, end='')
    print_prettier(turn, style='bold', end='')
    print_prettier(' to move\n', style=PRINCIPAL_STYLE)

def print_game(game: Game) -> None:
    '''
    Prints the game.

    Parameters
    ----------
    `game : Game`
        The game to print.
    '''

    print_prettier(str(game), style='bold')
    print_prettier(repr(game), style='fg:grey')

def print_game_over(game: Game, game_over: GameOver) -> None:
    '''
    Prints the game over message.

    Parameters
    ----------
    `game : Game`
        The game to print.
    `game_over : GameOver`
        The game over message.
    '''

    clear_playing()

    print_game(game)

    print_prettier('\nGame Over!', style=PRINCIPAL_STYLE, end='\n\n')

    print_prettier(game_over.score, style=SECONDARY_STYLE, end=' ')
    if game_over.winner:
        print_prettier(f'{game_over.winner.name.lower()} wins! by', style='bold', end=' ')
    else:
        print_prettier('It is a Draw! by', style='bold', end=' ')
    print_prettier(game_over.game_over_status.name.lower(), style='bold italic fg:grey', end='\n\n')

    get_text_input('Press enter to continue')

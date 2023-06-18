
from dataclasses import dataclass, field
from typing import Callable, Optional

from .helpers import console
from .helpers import config
from .helpers.custom_errors import IllegalMoveError, InvalidMoveInputError, InvalidFenError
from .models.game import Game, GameOver
from .models.game_modes.standard import StandardGame
from .models.game_modes.chess960 import Chess960Game


@dataclass(slots=True)
class System:
    '''
    A class that represents the system of the program.

    Attributes
    ----------
    `commands : dict[str, Callable[[], None]]`
        A dictionary of commands that the user can execute.
    
    Methods
    -------
    `menu() -> None`
        Displays the menu and executes the user's commands.
    `execute(command: str) -> None`
        Executes the given command.
    `select_game_mode() -> None`
        Displays the game mode selection menu and starts the game.
    '''

    commands: dict[str, Callable[[], None]] = field(kw_only = True, default_factory = dict)

    def __post_init__(self):

        self.commands['play'] = self.select_game_mode

        self.commands['help'] = lambda: print(
            '    Commands: \n'
            '\thelp - show this message\n'
            '\tplay - start a new game\n'
            '\texit - exit the program\n'
        )

        self.commands['options'] = self.options

        self.commands['exit'] = lambda: print('Exiting...\n')

    def menu(self) -> None:
        '''
        Displays the menu and executes the user's commands.

        Raises
        ------
        `AssertionError`
            If the user's command is not in the `commands` dictionary.
        '''

        console.clear()

        res: str = ''

        while res != 'exit':

            keys: list[str] = list(self.commands.keys())
            
            res = console.get_list_input('Select an option', keys)
            
            console.clear()

            self.execute(res)

    def execute(self, command: str) -> None:
        '''
        Executes the given command.

        Parameters
        ----------
        `command : str`
            The command to execute.

        Raises
        ------
        `AssertionError`
            If the user's command is not in the `commands` dictionary.
        '''

        assert command in self.commands
        
        self.commands[command]()

    def select_game_mode(self) -> None:
        '''
        Displays the game mode selection menu and starts the game.

        Raises
        ------
        `AssertionError`
            If the user's command is not in the `commands` dictionary.
        `ValueError`
            If the game mode is not recognized or if the user enters an unknown option in the play menu.
        '''

        console.clear_playing()
        
        res = console.get_list_input('Select a game mode', ['Standard Chess', 'Chess960'])

        console.clear_playing(res)

        game: Game

        try:
            if res == 'Standard Chess':
                game = StandardGame()
            elif res == 'Chess960': #TODO: Implement Chess960
                print('Chess960 is not yet implemented')
                game = Chess960Game()
            else:
                raise ValueError('Unknown game mode')
        except (ValueError, InvalidFenError) as e:
            print(e)
            return
        
        play_game(game, res)

    def options(self) -> None:
        '''
        Displays the options configuration menu.
        '''

        console.clear()

        back_option = 'back'
        style_option = 'game design'
        
        res = console.get_list_input('Select an option', [back_option, style_option])

        console.clear()

        if res == back_option:
            return
        elif res == style_option:
            unicode = 'unicode'
            small_board = 'small board'

            default_choices = []

            if config.unicode_pieces:
                default_choices.append(unicode)
            if config.small_board:
                default_choices.append(small_board)

            options: list[str] = console.get_choices_input(
                'Customize your board', [unicode, small_board], default_choices)

            config.unicode_pieces = unicode in options
            config.small_board = small_board in options


def play_game(game: Game, game_mode: str) -> None:
    '''
    Displays the game and executes the user's commands.

    Parameters
    ----------
    `game : Game`
        The game to play.
    `game_mode : str`
        The game mode to play.
    
    Raises
    ------
    `ValueError`
        If the user enters an unknown option in the play menu.
    '''

    playing = True

    msg: Optional[str] = None

    while playing:
        console.clear_playing(game_mode)

        console.print_game(game)
        console.print_turn(game.turn)

        if msg:
            print(msg)
            msg = None

        move_option = 'move'
        undo_option = '<--'
        redo_option = '-->'
        exit_option = 'exit'

        res = console.get_list_input('Select an option', [move_option, undo_option, redo_option, exit_option])

        if res == move_option:
            try:
                get_next_move(game)
            except (InvalidMoveInputError, IllegalMoveError) as e:
                msg = f'error: {e}\n'
            except GameOver as e:
                console.print_game_over(game, e)
                playing = False
                console.clear()


        elif res == undo_option:
            game.undo()

        elif res == redo_option:
            game.redo()
                
        elif res == exit_option:
            playing = False
            console.clear()
            
        else:
            raise ValueError('Unknown option')

def get_next_move(game: Game) -> None:
    '''
    Gets the next move from the user and executes it.

    Parameters
    ----------
    `game : Game`
        The game to play.
    
    Raises
    ------
    `InvalidMoveInputError`
        If the user enters an invalid move.
    `IllegalMoveError`
        If the user enters an illegal move.
    '''

    res = console.get_text_input('Enter a move')
    
    game.move(res)


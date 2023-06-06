
from dataclasses import dataclass, field
from typing import Callable

from .helpers.console import clear, clear_playing, get_text_input, get_list_input
from .models.game import Game
from .models.game_modes.standard import StandardGame
from .models.game_modes.chess960 import Chess960Game


@dataclass(slots=True)
class System:
    '''System class for the program.'''

    commands: dict[str, Callable[[], None]] = field(kw_only = True, default_factory = dict)

    def __post_init__(self):

        self.commands['play'] = self.select_game_mode

        self.commands['help'] = lambda: print(
            '    Commands: \n'
            '\thelp - show this message\n'
            '\tplay - start a new game\n'
            '\texit - exit the program\n'
        )

        self.commands['exit'] = lambda: print('Exiting...\n')

    def menu(self) -> None:
        clear()

        res: str = ''

        while res != 'exit':
            
            res = get_list_input('Select an option', self.commands.keys())
            
            clear()

            self.execute(res)

    def execute(self, command: str) -> None:
        assert command in self.commands
        
        self.commands[command]()

    def select_game_mode(self) -> None:
        clear_playing()
        
        res = get_list_input('Select a game mode', ['Standard Chess', 'Chess960'])

        clear_playing(res)

        game: Game
        
        if res == 'Standard Chess':
            game = StandardGame()
        elif res == 'Chess960':
            game = Chess960Game()
        else:
            raise Exception('Unknown game mode')
        
        play_game(game)

def play_game(game: Game) -> None:
    game_over = False

    while not game_over:
        clear_playing('Standard Chess')

        print(game)
        print(repr(game) + '\n')

        res = get_list_input('Select an option', ['<--', '-->', 'move', 'exit'])

        match res:
            case '<--':
                game.undo()
            case '-->':
                game.redo()
            case 'move':
                get_next_move(game)
            case 'exit':
                game_over = True
                clear()
            case _:
                raise Exception('Unknown option')

def get_next_move(game: Game) -> None:
    res = get_text_input('Enter a move')

    game.move(res)
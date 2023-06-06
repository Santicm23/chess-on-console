
from dataclasses import dataclass, field
from typing import Callable, List

import inquirer

from .helpers.console import clear, clear_playing
from .models.game import Game
from .models.game_modes.standard import StandardGame
from .models.game_modes.chess960 import Chess960Game


@dataclass(slots=True)
class System:
    '''System class for the program.'''

    commands: dict[str, Callable[[], None]] = field(kw_only = True, default_factory = lambda: {
            'play': play
        })
    
    menu_questions: List = field(init=False)

    def __post_init__(self):
        self.commands['help'] = lambda: print(
            '    Commands: \n'
            '\thelp - show this message\n'
            '\tplay - start a new game\n'
            '\texit - exit the program\n'
        )

        self.commands['exit'] = lambda: print('Exiting...\n')

        self.menu_questions = [
                inquirer.List('menu',
                        message='Options:',
                        choices=self.commands.keys(),
                    ),
            ]

    def menu(self) -> None:
        clear()

        command: str = ''

        while command != 'exit':
            
            answer = inquirer.prompt(self.menu_questions)

            assert answer is not None
            
            clear()
            command = answer['menu']
            self.execute(command)

    def execute(self, command: str) -> None:
        assert command in self.commands
        
        self.commands[command]()


def play() -> None:
    clear_playing()
    
    questions = [
        inquirer.List('game_mode',
                message = 'Select game mode:',
                choices = ['Standard Chess', 'Chess960'],
            ),
    ]
    answer = inquirer.prompt(questions)

    assert answer is not None

    clear_playing(answer['game_mode'])

    game: Game
    
    if answer['game_mode'] == 'Standard Chess':
        game = StandardGame()
    elif answer['game_mode'] == 'Chess960':
        game = Chess960Game()
    else:
        raise Exception('Unknown game mode')
    
    game.play()
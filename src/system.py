
from dataclasses import dataclass, field
from typing import Callable, List

import inquirer

from src.helpers.console import clear
from src.models.game import Game


@dataclass(slots=True)
class System:
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

            if answer is not None:
                clear()
                command = answer['menu']
                self.execute(command)

    def execute(self, command: str) -> None:
        if command == '':
            return
        elif command in self.commands:
            self.commands[command]()
        else:
            print(f'Unknown command: {command}')


def play() -> None:
    print('Playing chess!\n')
    
    questions = [
        inquirer.List('game_mode',
                message='Select game mode:',
                choices=['Standart', 'Chess960'],
            ),
    ]
    answers = inquirer.prompt(questions)

    clear()

    print('Playing chess!\n')

    game = Game()

    print(game)
    print(repr(game))
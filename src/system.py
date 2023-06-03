
from dataclasses import dataclass, field
from typing import Callable

import inquirer

from src.helpers.window import clear


@dataclass(slots=True)
class System:
    commands: dict[str, Callable[[], None]] = field(kw_only=True, default_factory=lambda: {
        'play': play
    })

    def __post_init__(self):
        self.commands['help'] = lambda: print(
            '    Commands: \n'
            '\thelp - show this message\n'
            '\tplay - start a new game\n'
            '\texit - exit the program\n'
        )

        self.commands['exit'] = lambda: print('Exiting...\n')

    def menu(self) -> None:
        clear()

        command: str = ''

        menu_msg: str = '\n\t ---- Welcome to the Chess game! ---- \n\n'

        print(menu_msg)
        while command != 'exit':
            questions = [
                inquirer.List('menu',
                        message='Options:',
                        choices=self.commands.keys(),
                    ),
            ]
            answer = inquirer.prompt(questions)

            if answer is not None:
                clear()
                print(menu_msg)
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
                message='Selectgame mode:',
                choices=['Standart', 'Chess960'],
            ),
    ]
    answers = inquirer.prompt(questions)
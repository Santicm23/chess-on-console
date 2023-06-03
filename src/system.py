
import inquirer
from dataclasses import dataclass, field
from typing import Callable


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
            '\texit - exit the program'
        )

        self.commands['exit'] = lambda: print('Exiting...')

    def execute(self, command: str):
        if command == '':
            pass
        elif command in self.commands:
            self.commands[command]()
        else:
            print(f'Unknown command: {command}')


def play() -> None:
    print('Playing chess!')
    
    questions = [
    inquirer.List('size',
                    message='Selectgame mode:',
                    choices=['Standart', 'Chess960'],
                ),
    ]
    answers = inquirer.prompt(questions)
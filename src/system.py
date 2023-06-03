
from dataclasses import dataclass, field
from typing import Callable


@dataclass(slots=True)
class System:
    commands: dict[str, Callable[[], None]] = field(kw_only=True, default_factory=lambda: {
        'play': commandPlay
    })

    def __post_init__(self):
        self.commands['help'] = commandHelp
        self.commands['exit'] = commandExit

    def execute(self, command: str):
        if command == '':
            pass
        elif command in self.commands:
            self.commands[command]()
        else:
            print(f'Unknown command: {command}')
    
def commandHelp() -> None:
    print('    Commands:')
    print('\thelp - show this message')
    print('\tplay - start a new game')
    print('\texit - exit the program')

def commandPlay() -> None:
    ...

def commandExit() -> None:
    print('Goodbye!')
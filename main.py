
import inquirer
from src.system import System


def main() -> None:
    command: str = ''

    print('Play chess on the command line!')
    while command != 'exit':

        command = input('--> ')

        system = System()

        system.execute(command)


if __name__ == '__main__':
    main()
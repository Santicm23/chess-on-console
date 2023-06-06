
from ..game import Game


class Chess960Game(Game):
    '''Chess960 game'''
    
    def play(self) -> None:
        print(self)
        print(repr(self))
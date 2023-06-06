
from ..game import Game
from ...helpers.console import clear_playing


class StandardGame(Game):
    '''Standard chess game.'''
    
    def play(self) -> None:
        game_over = False

        while not game_over:
            clear_playing('Standard Chess')

            print(self)
            print(repr(self))

            

            game_over = True

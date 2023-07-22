'''./src/models/game_modes/chess960.py'''

import random

from . import StandardGame


class Chess960Game(StandardGame):
    '''Chess960 game'''

    def __init__(self) -> None:
        super().__init__(self.__class__.generate_random_fen())
    
    @staticmethod
    def generate_random_fen() -> str:
        '''
        Generates a random FEN string for a Chess960 game.

        Returns
        -------
        `str`
            The generated FEN string.
        '''

        fen = ''
        remain_pieces = ['r', 'n', 'b', 'q', 'b', 'n', 'r']
        last_piece = ''
        
        while not last_piece == 'r':
            last_piece = remain_pieces.pop(random.randint(0, len(remain_pieces)-1))
            fen += last_piece
        
        remain_pieces.remove('r')
        
        remain_pieces.append('k')
        
        while not last_piece == 'k':
            last_piece = remain_pieces.pop(random.randint(0, len(remain_pieces)-1))
            fen += last_piece
        
        remain_pieces.append('r')
        
        while not len(remain_pieces) == 0:
            fen += remain_pieces.pop(random.randint(0, len(remain_pieces)-1))
        
        return f'{fen}/pppppppp/8/8/8/8/PPPPPPPP/{fen.upper()} w KQkq - 0 1'


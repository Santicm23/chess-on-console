'''./src/models/game_modes/chess960.py'''

import random

from .standard import StandardGame


class Chess960Game(StandardGame):
    '''Chess960 game'''

    def __init__(self) -> None:
        super().__init__(self.generate_random_fen())
    
    def generate_random_fen(self) -> str:
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


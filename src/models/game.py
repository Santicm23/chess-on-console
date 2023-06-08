
import re
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Optional, Type, Generator, Callable

from .board import Board
from .piece import Piece
from .pieces.standard import King
from ..helpers.constants import Position, Color


@dataclass(slots=True)
class Game(ABC):
    '''Abstract class for all games.'''

    start_fen: str = field(init = True)
    board: Board = field(init = False)
    turn: str = field(init = False)
    castling: str = field(init = False)
    en_passant: str = field(init = False)
    halfmove_clock: int = field(init = False)
    fullmove_number: int = field(init = False)
    pieces_from_fen: dict[str, Type[Piece]] = field(init = False, default_factory = lambda: {'k': King})

    def __post_init__(self) -> None:
        pass

    def __str__(self) -> str:
        return str(self.board)

    def __repr__(self) -> str:
        return f'{repr(self.board)} {self.turn} {self.castling} {self.en_passant} {self.halfmove_clock} {self.fullmove_number}'

    def __getitem__(self, pos: str) -> Optional[Piece]:
        return self.board[pos]

    def __setitem__(self, pos: str, piece: Piece) -> None:
        self.board[pos] = piece

    def __delitem__(self, pos: str) -> None:
        del self.board[pos]

    def __contains__(self, piece: Piece) -> bool:
        return piece in self.board
    
    def __iter__(self) -> Generator[Optional[Piece], None, None]:
        return iter(self.board)
    
    def __len__(self) -> int:
        return len(self.board)
    
    def change_turn(self) -> None:
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'
            self.fullmove_number += 1

    def parse_move(self, move: str) -> tuple[Piece, Position, Optional[Piece], Optional[Type[Piece]]]:
        '''Returns the piece, start position, captured piece and promotion piece of a move.'''

        if not re.match(
            r'^([NBRQK]?[a-h]?[1-8]?x?[a-h][1-8](=[NBRQ])?|O(-O){1,2})$',
            move
        ):
            raise ValueError('Invalid move')
        
        piece: Optional[Piece] = None
        pos: Position
        captured_piece: Optional[Piece] = None
        promotion_piece: Optional[Type[Piece]] = None
        
        if self.turn == 'w':
            color = Color.WHITE
        else:
            color = Color.BLACK
        
        if move[0] == 'O':
            piece = self.board.pieces[color][0]
            col: str = 'g' if move == 'O-O' else 'c'
            row: int = 1 if color == Color.WHITE else 8
            pos = Position(col, row)
        
        else:
            pos_index: int
            if '=' in move:
                if move[0] in 'NBRQK':
                    raise ValueError('Invalid move')
                
                promotion_piece = self.pieces_from_fen[move[-1]]

                pos = Position(move[-4], int(move[-3]))

                pos_index = len(move) - 4
            
            else:
                pos = Position(move[-2], int(move[-1]))
                pos_index = len(move) - 2

            captured_piece = self[str(pos)]

            
            if 'x' in move and captured_piece is None:
                raise ValueError('Invalid move')
            
            condicions: Callable[[str], bool]

            if move[pos_index - 2] in 'abcdefgh' and move[pos_index - 1] in '12345678':
                condicions = lambda sqr: sqr[0] == move[pos_index - 2] and sqr[1] == move[pos_index - 1]
            elif move[pos_index - 1] in 'abcdefgh':
                condicions = lambda sqr: sqr[0] == move[pos_index - 1]
            elif move[pos_index - 1] in '12345678':
                condicions = lambda sqr: sqr[1] == move[pos_index - 1]
            else:
                condicions = lambda sqr: True
            
            for p in self:
                if p is not None and p.color == color and str(p).upper() == move[0] and condicions(str(p.pos)):
                    piece = p
                    break
        
        if piece is None :#or pos not in piece.legal_moves:
            raise ValueError('Invalid move')
        
        return piece, pos, captured_piece, promotion_piece

    def undo(self) -> None:
        self.board.undo()
    
    def redo(self) -> None:
        self.board.redo()

    @abstractmethod
    def move(self, move: str) -> None:...


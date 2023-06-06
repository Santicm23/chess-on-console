
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Optional, Type

from .board import Board, Piece
from .pieces.standard import King


@dataclass(slots=True)
class Game(ABC):
    '''Abstract class for all games.'''

    start_fen: str = field(default = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    board: Board = field(init = False)
    turn: str = field(init = False)
    castling: str = field(init = False)
    en_passant: str = field(init = False)
    halfmove_clock: int = field(init = False)
    fullmove_number: int = field(init = False)
    pieces_from_fen: dict[str, Type[Piece]] = field(init = False, default_factory = lambda: {'k': King})

    def __post_init__(self):
        fen, self.turn, self.castling, self.en_passant, halfmove_clock, fullmove_number = self.start_fen.split()
        self.board = Board(fen, self.pieces_from_fen)
        self.halfmove_clock = int(halfmove_clock)
        self.fullmove_number = int(fullmove_number)

    def __str__(self) -> str:
        return str(self.board)

    def __repr__(self) -> str:
        return f'{repr(self.board)} {self.turn} {self.castling} {self.en_passant} {self.halfmove_clock} {self.fullmove_number}'

    def __getitem__(self, pos: tuple[str, int]) -> Optional[Piece]:
        return self.board[pos]

    def __setitem__(self, pos: tuple[str, int], piece: Piece) -> None:
        self.board[pos] = piece

    def __delitem__(self, pos: tuple[str, int]) -> None:
        del self.board[pos]

    def move_is_legal(self, pos: tuple[str, int], piece: Piece):...

    def update_piece_lm(self, piece: Piece):...

    def update_legal_moves(self):...

    def update_right_castle(self, piece: Piece):
        # if piece.color == 'w':
        #     self.castling = self.castling.replace('K', '')
        # else:
        #     self.castling = self.castling.replace('k', '')
        ...

    def update_en_passant(self, pos: tuple[str, int], piece: Piece):
        # if piece.color == 'w':
        #     self.en_passant = col_to_int(pos[0]) + 1
        # else:
        #     self.en_passant = col_to_int(pos[0]) - 1
        ...

    @abstractmethod
    def play(self) -> None:...
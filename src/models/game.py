
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Self

from .board import Board
from .pieces import Piece


@dataclass(slots=True)
class Game(ABC):
    start_fen: str = field(default = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    board: Board = field(init = False)
    turn: str = field(init = False)
    castling: str = field(init = False)
    en_passant: str = field(init = False)
    halfmove_clock: int = field(init = False)
    fullmove_number: int = field(init = False)

    def __post_init__(self):
        fen, self.turn, self.castling, self.en_passant, halfmove_clock, fullmove_number = self.start_fen.split()
        self.board = Board(fen)
        self.halfmove_clock = int(halfmove_clock)
        self.fullmove_number = int(fullmove_number)

    def __str__(self):
        return str(self.board)

    def __repr__(self):
        return f'{repr(self.board)} {self.turn} {self.castling} {self.en_passant} {self.halfmove_clock} {self.fullmove_number}'

    def __getitem__(self, pos: tuple[str, int]):
        return self.board[pos]

    def __setitem__(self, pos: tuple[str, int], piece: Piece):
        self.board[pos] = piece

    def __delitem__(self, pos: tuple[str, int]):
        del self.board[pos]

    def move_is_legal(self, pos: tuple[str, int], piece: Piece):...

    def update_piece_lm(self, piece: Piece):...

    def update_legal_moves(self):...

    def update_right_castle(self, piece: Piece):...

    def update_en_passant(self, pos: tuple[str, int], piece: Piece):...

    @abstractmethod
    def play(self) -> None:...
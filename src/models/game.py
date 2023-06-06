
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Optional, Type

from .board import Board
from .piece import Piece
from .pieces.standard import King


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

    def __getitem__(self, pos: tuple[str, int]) -> Optional[Piece]:
        return self.board[pos]

    def __setitem__(self, pos: tuple[str, int], piece: Piece) -> None:
        self.board[pos] = piece

    def __delitem__(self, pos: tuple[str, int]) -> None:
        del self.board[pos]

    @abstractmethod
    def play(self) -> None:...
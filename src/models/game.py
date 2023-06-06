
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Optional, Type, Generator

from .board import Board
from .piece import Piece
from .pieces.standard import King
from ..helpers.constants import Position


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

    def __getitem__(self, pos: Position) -> Optional[Piece]:
        return self.board[pos]

    def __setitem__(self, pos: Position, piece: Piece) -> None:
        self.board[pos] = piece

    def __delitem__(self, pos: Position) -> None:
        del self.board[pos]

    def __contains__(self, piece: Piece) -> bool:
        return piece in self.board
    
    def __iter__(self) -> Generator[Optional[Piece], None, None]:
        return iter(self.board)
    
    def __len__(self) -> int:
        return len(self.board)
    
    def undo(self) -> None:
        self.board.undo()
    
    def redo(self) -> None:
        self.board.redo()

    @abstractmethod
    def move(self, move: str) -> None:...
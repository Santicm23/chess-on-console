
from __future__ import annotations
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Optional, Protocol

from ..helpers.constants import Color, Position


class Board(Protocol):
    def __getitem__(self, pos: Position) -> Optional[Piece]:
        '''Get piece at position'''


@dataclass(slots=True)
class Piece(ABC):
    '''Abstract class for all pieces'''

    color: Color
    pos: Position
    legal_moves: list[Position] = field(init = False, default_factory = list)

    def __str__(self) -> str:
        return self.__class__.__name__[0].upper() if self.color == Color.WHITE else self.__class__.__name__[0].lower()
    
    def is_legal(self, pos: Position) -> bool:
        return pos in self.legal_moves
    
    def move(self, pos: Position) -> None:
        self.pos = pos
    
    @abstractmethod
    def can_move(self, board: Board, pos: Position) -> bool:...
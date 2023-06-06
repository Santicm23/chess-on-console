
from __future__ import annotations
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Optional, Protocol

from ..helpers.constants import Color


class Board(Protocol):
    def __getitem__(self, pos: tuple[str, int]) -> Optional[Piece]:
        '''Get piece at position'''


@dataclass(slots=True)
class Piece(ABC):
    '''Abstract class for all pieces'''

    color: Color
    pos: tuple[str, int]
    legal_moves: list[tuple[int, int]] = field(init = False, default_factory = list)

    def __str__(self) -> str:
        return self.__class__.__name__[0].upper() if self.color == Color.WHITE else self.__class__.__name__[0].lower()
    
    def __eq__(self, other: Piece) -> bool:
        return str(self) == str(other)
    
    def is_legal(self, pos: tuple[str, int]) -> bool:
        return pos in self.legal_moves
    
    def move(self, pos: tuple[str, int]) -> None:
        self.pos = pos
    
    @abstractmethod
    def can_move(self, board: Board, pos: tuple[str, int]) -> bool:...
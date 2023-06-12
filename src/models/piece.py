
from __future__ import annotations
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Optional, Protocol

from ..helpers.constants import Color, Position


class Board(Protocol): #TODO: correct the type hints
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
    
    def is_legal_move(self, pos: str | Position) -> bool:
        if isinstance(pos, str) and pos[1].isdigit():
            pos = Position(pos[0], int(pos[1]))
        return pos in self.legal_moves
    
    def move(self, pos: Position) -> None:
        self.pos = pos
    
    @abstractmethod
    def can_move(self, board: Board, pos: Position) -> bool:
        '''Returns True if the piece can move to the given position.'''
        if self.pos == pos:
            return False


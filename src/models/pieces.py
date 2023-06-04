
from dataclasses import dataclass, field
from typing import Self, Type
from abc import ABC, abstractmethod

from helpers.constants import Color


@dataclass(slots=True)
class Piece(ABC):
    color: Color
    pos: tuple[int, int]
    legal_moves: list[tuple[int, int]] = field(init=False, default_factory=list)

    def __str__(self) -> str:
        return self.__repr__()
    
    def __repr__(self) -> str:
        return self.__class__.__name__[0].upper() if self.color == Color.WHITE else self.__class__.__name__[0].lower()
    
    def __eq__(self, other: Self) -> bool:
        return str(self) == str(other)
    
    def is_legal(self, pos: tuple[int, int]) -> bool:
        return pos in self.legal_moves
    
    def move(self, pos: tuple[int, int]) -> None:
        self.pos = pos
    
    @abstractmethod
    def movement(self, pos: tuple[int, int]) -> bool:...


@dataclass(slots=True)
class Pawn(Piece):
    
    def movement(self, pos: tuple[int, int]) -> bool:
        x, y = self.pos
        new_x, new_y = pos

        if self.color == Color.WHITE:
            if new_x == x and new_y == y + 1:
                return True
            elif new_x == x and new_y == y + 2 and y == 1:
                return True
            elif new_x == x + 1 and new_y == y + 1:
                return True
            elif new_x == x - 1 and new_y == y + 1:
                return True
        elif self.color == Color.BLACK:
            if new_x == x and new_y == y - 1:
                return True
            elif new_x == x and new_y == y - 2 and y == 6:
                return True
            elif new_x == x + 1 and new_y == y - 1:
                return True
            elif new_x == x - 1 and new_y == y - 1:
                return True
        return False

    def promote(self, piece_type: Type[Piece]) -> None:
        self.__class__ = piece_type


@dataclass(slots=True)
class knight(Piece):

    def __repr__(self) -> str:
        return 'N' if self.color == Color.WHITE else 'n'
    
    def movement(self, pos: tuple[int, int]) -> bool:
        x, y = self.pos
        new_x, new_y = pos

        if (new_x, new_y) in [(x + 1, y + 2), (x + 2, y + 1), (x + 2, y - 1), (x + 1, y - 2),
                              (x - 1, y - 2), (x - 2, y - 1), (x - 2, y + 1), (x - 1, y + 2)]:
            return True
        return False


@dataclass(slots=True)
class Bishop(Piece):

    def movement(self, pos: tuple[int, int]) -> bool:
        x, y = self.pos
        new_x, new_y = pos

        if abs(new_x - x) == abs(new_y - y):
            return True
        return False


@dataclass(slots=True)
class Rook(Piece):

    def movement(self, pos: tuple[int, int]) -> bool:
        x, y = self.pos
        new_x, new_y = pos

        if new_x == x or new_y == y:
            return True
        return False


@dataclass(slots=True)
class Queen(Piece):

    def movement(self, pos: tuple[int, int]) -> bool:
        x, y = self.pos
        new_x, new_y = pos

        if abs(new_x - x) == abs(new_y - y) or new_x == x or new_y == y:
            return True
        return False


@dataclass(slots=True)
class King(Piece):

    def movement(self, pos: tuple[int, int]) -> bool:
        x, y = self.pos
        new_x, new_y = pos

        if abs(new_x - x) <= 1 and abs(new_y - y) <= 1:
            return True
        return False
    
    def castle(self, rook: Rook) -> None:
        self.pos = rook.pos
        rook.pos = self.pos
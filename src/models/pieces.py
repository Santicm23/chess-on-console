
from dataclasses import dataclass, field
from typing import Self, Type
from abc import ABC, abstractmethod

from ..helpers.constants import Color
from ..helpers.functions import col_to_int, int_to_col


@dataclass(slots=True)
class Piece(ABC):
    '''Abstract class for all pieces.'''

    color: Color
    pos: tuple[str, int]
    legal_moves: list[tuple[int, int]] = field(init=False, default_factory=list)

    @classmethod
    def from_fen(cls, code: str, pos: tuple[str, int]) -> Self:
        color = Color.WHITE if code.isupper() else Color.BLACK
        return {
            'p': Pawn(color, pos),
            'n': Knight(color, pos),
            'b': Bishop(color, pos),
            'r': Rook(color, pos),
            'q': Queen(color, pos),
            'k': King(color, pos)
        }[code.lower()]

    def __str__(self) -> str:
        return self.__class__.__name__[0].upper() if self.color == Color.WHITE else self.__class__.__name__[0].lower()
    
    def __eq__(self, other: Self) -> bool:
        return str(self) == str(other)
    
    def is_legal(self, pos: tuple[str, int]) -> bool:
        return pos in self.legal_moves
    
    def move(self, pos: tuple[str, int]) -> None:
        self.pos = pos
    
    @abstractmethod
    def can_move(self, pos: tuple[str, int]) -> bool:...


@dataclass(slots=True)
class Pawn(Piece):
    '''Pawn piece.'''
    
    def can_move(self, pos: tuple[str, int]) -> bool:
        x, y = self.pos
        new_x, new_y = pos

        x = col_to_int(x)
        new_x = col_to_int(new_x)

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
class Knight(Piece):
    '''Knight piece.'''

    def __str__(self) -> str:
        return 'N' if self.color == Color.WHITE else 'n'
    
    def can_move(self, pos: tuple[str, int]) -> bool:
        x, y = self.pos
        new_x, new_y = pos

        x = col_to_int(x)
        new_x = col_to_int(new_x)

        if (new_x, new_y) in [(x + 1, y + 2), (x + 2, y + 1), (x + 2, y - 1), (x + 1, y - 2),
                              (x - 1, y - 2), (x - 2, y - 1), (x - 2, y + 1), (x - 1, y + 2)]:
            return True
        return False


@dataclass(slots=True)
class Bishop(Piece):
    '''Bishop piece.'''

    def can_move(self, pos: tuple[str, int]) -> bool:
        x, y = self.pos
        new_x, new_y = pos

        x = col_to_int(x)
        new_x = col_to_int(new_x)

        if abs(new_x - x) == abs(new_y - y):
            return True
        return False


@dataclass(slots=True)
class Rook(Piece):
    '''Rook piece.'''

    has_moved: bool = field(init=False, default=False)

    def can_move(self, pos: tuple[int, int]) -> bool:
        x, y = self.pos
        new_x, new_y = pos

        if new_x == x or new_y == y:
            return True
        return False

    def move(self, pos: tuple[str, int]) -> None:
        super().move(pos)
        self.has_moved = True


@dataclass(slots=True)
class Queen(Piece):
    '''Queen piece.'''

    def can_move(self, pos: tuple[str, int]) -> bool:
        x, y = self.pos
        new_x, new_y = pos

        x = col_to_int(x)
        new_x = col_to_int(new_x)

        if abs(new_x - x) == abs(new_y - y) or new_x == x or new_y == y:
            return True
        return False


@dataclass(slots=True)
class King(Piece):
    '''King piece.'''

    has_moved: bool = field(init=False, default=False)
    check: bool = field(init=False, default=False)

    def can_move(self, pos: tuple[str, int]) -> bool:
        x, y = self.pos
        new_x, new_y = pos

        x = col_to_int(x)
        new_x = col_to_int(new_x)

        if abs(new_x - x) <= 1 and abs(new_y - y) <= 1:
            return True
        return False
    
    def update_check(self, check: bool) -> None:
        self.check = check

    def can_castle(self, rook: Rook) -> bool:
        return not (self.has_moved or rook.has_moved or self.check) and rook.color == self.color

    def castle(self, rook: Rook) -> None:
        x, y = self.pos
        rook_x, rook_y = rook.pos

        x = col_to_int(x)
        rook_x = col_to_int(rook_x)

        if rook_x < x:
            self.move((int_to_col(x - 2), y))
            rook.move((int_to_col(x - 1), y))
        else:
            self.move((int_to_col(x + 2), y))
            rook.move((int_to_col(x + 1), y))
    
    def move(self, pos: tuple[str, int]) -> None:
        super().move(pos)
        self.has_moved = True
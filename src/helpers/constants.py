'''./src/helpers/constants.py'''

from dataclasses import dataclass
from enum import Enum, auto
from typing import Self, Literal

from .functions import col_to_int, int_to_col


class Color(Enum):
    WHITE = auto(),
    BLACK = auto()


class GameOverStatus(Enum):
    CHECKMATE = auto(),
    STALEMATE = auto(),
    INSUFFICIENT_MATERIAL = auto(),
    FIFTY_MOVE_RULE = auto(),
    THREEFOLD_REPETITION = auto(),
    FIVEFOLD_REPETITION = auto()


COLOR_MAP = {
    'w': Color.WHITE,
    'b': Color.BLACK
}

UNICODE_PIECES: dict[str, str] = {
    'p': '♙', 'P': '♟',
    'n': '♘', 'N': '♞',
    'b': '♗', 'B': '♝',
    'r': '♖', 'R': '♜',
    'q': '♕', 'Q': '♛',
    'k': '♔', 'K': '♚'
}


@dataclass
class Position(tuple[str, int]):
    '''
    Position on the board

    Attributes
    ----------
    `col: str`
        The column of the position
    `row: int`
        The row of the position

    Operators
    ---------
    `__str__() -> str`
        Returns the string representation of the position.
    `__getitem__(index: Literal['row', 'col']) -> int | str`
        Returns the row or column of the position.
    `__eq__(other: Position) -> bool`
        Returns True if the positions are equal.
    `__add__(other: tuple[int, int]) -> Position`
        Returns the position after adding the given tuple to the position.
    `__sub__(other: tuple[int, int]) -> Position`
        Returns the position after subtracting the given tuple from the position.
    `__ne__(other: Position) -> bool`
        Returns True if the positions are not equal.
    `__next__() -> Position`
        Returns the next position.
    
    Methods
    -------
    `diff(other: Position) -> tuple[int, int]`
        Returns the difference between the positions.
    '''

    col: str
    row: int

    def __new__(cls, col: str, row: int) -> Self:
        return super().__new__(cls, (col, row))

    def __init__(self, col: str, row: int) -> None:
        self.col: str = col
        self.row: int = row

    def __str__(self) -> str:
        return f'{self.col}{self.row}'
    
    def __getitem__(self, index: Literal['row', 'col']) -> int | str:
        return getattr(self, index)
    
    def __eq__(self, other: Self) -> bool:
        return str(self) == str(other)

    def __add__(self, other: tuple[int, int]) -> Self:
        return Position(int_to_col(col_to_int(self.col) + other[0]), self.row + other[1])
    
    def __sub__(self, other: tuple[int, int]) -> Self:
        return Position(int_to_col(col_to_int(self.col) - other[0]), self.row - other[1])
    
    def __ne__(self, other: Self) -> bool:
        return not self == other
    
    def __next__(self) -> Self:
        if self.col == 'h':
            if self.row == 8:
                raise StopIteration
            return Position('a', self.row + 1)
        return Position(int_to_col(col_to_int(self.col) + 1), self.row)

    def diff(self, other: Self) -> tuple[int, int]:
        return (col_to_int(self.col) - col_to_int(other.col), self.row - other.row)

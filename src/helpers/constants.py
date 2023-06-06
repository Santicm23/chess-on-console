
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Self, Literal

from ..helpers.functions import col_to_int, int_to_col


class Color(Enum):
    WHITE = auto(),
    BLACK = auto()


class Position(tuple[str, int]):

    def __new__(cls, col: str, row: int) -> Self:
        return super().__new__(cls, (row, col))

    def __init__(self, col: str, row: int) -> None:
        self.row: int = row
        self.col: str = col

    def __str__(self) -> str:
        return f'{self.col}{self.row}'
    
    def __getitem__(self, index: Literal['row', 'col']) -> Any:
        return getattr(self, index)
    
    def __eq__(self, other: Self) -> bool:
        return str(self) == str(other)

    def __add__(self, other: tuple[int, int]) -> Self:
        return Position(int_to_col(col_to_int(self.col) + other[0]), self.row + other[1])
    
    def __sub__(self, other: tuple[int, int]) -> Self:
        return Position(int_to_col(col_to_int(self.col) - other[0]), self.row - other[1])
    
    def __ne__(self, other: Self) -> bool:
        return not self == other
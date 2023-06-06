
from dataclasses import dataclass, field
from typing import List, Optional, Generator, Type, Self
from itertools import groupby
from abc import ABC, abstractmethod

from ..helpers.functions import col_to_int, int_to_col
from ..helpers.constants import Color


@dataclass(slots=True)
class Piece(ABC):
    '''Abstract class for all pieces.'''

    color: Color
    pos: tuple[str, int]
    legal_moves: list[tuple[int, int]] = field(init=False, default_factory=list)

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
class Board:
    '''Chess board.'''

    matrix: List[List[Optional[Piece]]]
    pieces: dict[Color, List[Piece]] = field(default_factory = lambda: {
        Color.WHITE: [],
        Color.BLACK: []
    })

    def __init__(self, fen: str, pieces_from_fen: dict[str, Type[Piece]]):
        self.matrix = [[None for _ in range(8)] for _ in range(8)]
        self.load_fen(fen, pieces_from_fen)
    
    def load_fen(self, fen: str, pieces_from_fen: dict[str, Type[Piece]]) -> None:
        fen_list = fen.split('/')
        for row, fen_row in zip(self.matrix, fen_list):
            col = 0
            for char in fen_row:
                if char.isdigit():
                    col += int(char)
                else:
                    if char.isupper():
                        piece = pieces_from_fen[char.lower()](Color.WHITE, (int_to_col(col), 8 - self.matrix.index(row)))
                    else:
                        piece = pieces_from_fen[char.lower()](Color.BLACK, (int_to_col(col), 8 - self.matrix.index(row)))
                    
                    row[col] = piece

                    index = 0 if isinstance(piece, pieces_from_fen['k']) else -1

                    self.pieces[piece.color].insert(index, piece)
                    
                    col += 1

    def __str__(self) -> str:
        border: str = '+---+---+---+---+---+---+---+---+\n'
        return border + border.join(
                '| ' + ' | '.join(str(piece) if piece is not None else ' ' for piece in row) + ' |\n'
                for row in self.matrix
            ) + border

    def __repr__(self) -> str:
        return '/'.join(
            ''.join(
                str(sum(1 for _ in group)) if piece is None else str(piece)
                for piece, group in groupby(row)
            )
            for row in self.matrix
        )

    def __getitem__(self, pos: tuple[str, int]) -> Optional[Piece]:
        col, row = pos
        return self.matrix[row - 1][col_to_int(col)]

    def __setitem__(self, pos: tuple[str, int], piece: Piece) -> None:
        col, row = pos
        self.matrix[row - 1][col_to_int(col)] = piece

    def __delitem__(self, pos: tuple[str, int]) -> None:
        col, row = pos
        self.matrix[row - 1][col_to_int(col)] = None

    def __iter__(self) -> Generator[Optional[Piece], None, None]:
        for row in self.matrix:
            for piece in row:
                yield piece
    
    def __contains__(self, piece: Piece) -> bool:
        return piece in self.pieces[Color.WHITE] or piece in self.pieces[Color.BLACK]
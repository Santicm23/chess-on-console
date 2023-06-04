
from dataclasses import dataclass, field
from typing import List, Optional
from itertools import groupby

from src.models.pieces import Piece
from src.helpers.functions import col_to_int, int_to_col


@dataclass(slots=True)
class Board:
    matrix: List[List[Optional[Piece]]] = field(init = False)

    def __init__(self, fen: str):
        self.matrix = [[None for _ in range(8)] for _ in range(8)]
        self.load_fen(fen)
    
    def load_fen(self, fen: str) -> None:
        fen_list = fen.split('/')
        for row, fen_row in zip(self.matrix, fen_list):
            col = 0
            for char in fen_row:
                if char.isdigit():
                    col += int(char)
                else:
                    row[col] = Piece.from_fen(char, (int_to_col(col), 8 - self.matrix.index(row)))
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

    def __getitem__(self, pos: tuple[str, int]):
        col, row = pos
        return self.matrix[row - 1][col_to_int(col)]

    def __setitem__(self, pos: tuple[str, int], piece: Piece):
        col, row = pos
        self.matrix[row - 1][col_to_int(col)] = piece

    def __delitem__(self, pos: tuple[str, int]):
        col, row = pos
        self.matrix[row - 1][col_to_int(col)] = None

    def __iter__(self):
        for row in self.matrix:
            for piece in row:
                yield piece
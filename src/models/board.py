
from dataclasses import dataclass, field
from typing import List, Optional
from itertools import groupby

from pieces import Piece
from helpers.functions import col_to_int


@dataclass(slots=True)
class Board:
    matrix: List[List[Optional[Piece]]] = field(
            default_factory = lambda: [[None for _ in range(8)] for _ in range(8)]
        )

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

    def __setitem__(self, pos: tuple[str, int], piece: Piece):...

    def __delitem__(self, pos: tuple[str, int]):...

    def __iter__(self):...
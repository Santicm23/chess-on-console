
from dataclasses import dataclass, field
from typing import List, Optional, Generator, Type, Self
from itertools import groupby

from ..helpers.functions import col_to_int, int_to_col
from ..helpers.constants import Color, Position
from .piece import Piece
from .pieces.standard import King, Rook


@dataclass(slots=True)
class Board: #TODO: correct the type hints
    '''Chess board'''

    matrix: List[List[Optional[Piece]]] = field(init = False, default_factory = lambda: [[None] * 8 for _ in range(8)])
    pieces: dict[Color, List[Piece]] = field(init = False, default_factory = lambda: {
        Color.WHITE: [], Color.BLACK: []
    })
    
    @classmethod
    def from_fen(cls, fen: str, pieces_from_fen: dict[str, Type[Piece]]) -> Self:
        board = cls()
        board.load_fen(fen, pieces_from_fen)
        return board
    
    def load_fen(self, fen: str, pieces_from_fen: dict[str, Type[Piece]]) -> None:
        fen_list = fen.split('/')
        
        i_row = 8
        for row, fen_row in zip(self.matrix, fen_list):
            i_col = 0

            for char in fen_row:
                if char.isdigit():
                    i_col += int(char)
                    continue

                color = Color.WHITE if char.isupper() else Color.BLACK

                piece = pieces_from_fen[char.lower()](color, Position(int_to_col(i_col), i_row))
                
                row[i_col] = piece

                index = 0 if isinstance(piece, pieces_from_fen['k']) else -1

                self.pieces[piece.color].insert(index, piece)
                
                i_col += 1
            
            i_row -= 1

    def __str__(self) -> str:
        border: str = '  +---+---+---+---+---+---+---+---+\n'
        rank_labels: str = '    a   b   c   d   e   f   g   h\n'
        return border + border.join(
                f'{8 - i} | ' + ' | '.join(str(piece) if piece is not None else ' ' for piece in row) + ' |\n'
                for i, row in enumerate(self.matrix)
            ) + border + rank_labels

    def __repr__(self) -> str:
        return '/'.join(
            ''.join(
                str(sum(1 for _ in group)) if piece is None else str(piece)
                for piece, group in groupby(row)
            )
            for row in self.matrix
        )

    def __getitem__(self, pos: str | Position) -> Optional[Piece]:
        if isinstance(pos, str):
            pos = Position(pos[0], int(pos[1]))
        col, row = pos
        return self.matrix[8 - row][col_to_int(col)]

    def __setitem__(self, pos: str | Position, piece: Optional[Piece]) -> None:
        if isinstance(pos, str):
            pos = Position(pos[0], int(pos[1]))
        col, row = pos
        self.matrix[8 - row][col_to_int(col)] = piece

    def __delitem__(self, pos: str | Position) -> None:
        if isinstance(pos, str):
            pos = Position(pos[0], int(pos[1]))
        col, row = pos
        self.matrix[8 - row][col_to_int(col)] = None

    def __iter__(self) -> Generator[Optional[Piece], None, None]:
        for row in self.matrix:
            for piece in row:
                yield piece
    
    def __contains__(self, piece: Piece) -> bool:
        return piece in self.pieces[Color.WHITE] or piece in self.pieces[Color.BLACK]

    def __len__(self) -> int:
        return sum(len(pieces) for pieces in self.pieces.values())

    def get_king(self, color: Color) -> King:
        king = self.pieces[color][0]
        if isinstance(king, King):
            return king
        raise TypeError(f'Expected King, got {type(self.pieces[color][0])}')

    def move(self, piece: Piece, pos: Position) -> None:
        if isinstance(piece, King) and abs(piece.pos.diff(pos)[0]) == 2:
            rook = self[pos + (1, 0)] if pos.col == 'g' else self[pos - (2, 0)]
            castle_pos = Position('f' if pos.col == 'g' else 'd', pos.row)
            if rook is not None and isinstance(rook, Rook) and rook.color == piece.color:
                del self[piece.pos]
                del self[rook.pos]
                piece.castle(rook)
                self[castle_pos] = rook
                self[pos] = piece
            else:
                raise ValueError('Invalid castling')
        else:
            del self[piece.pos]
            piece.move(pos)
            self[pos] = piece

    def undo(self) -> None:
        pass

    def redo(self) -> None:
        pass


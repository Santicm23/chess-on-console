
from dataclasses import dataclass, field
from typing import List, Optional, Generator, Type, Self
from itertools import groupby
from functools import reduce

from ..helpers.functions import col_to_int, int_to_col
from ..helpers.constants import Color, Position, SPECIAL_CHARS
from .piece import Piece
from .pieces.standard import King, Rook, Pawn


@dataclass(slots=True)
class Board:
    '''
    Chess board

    Attributes
    ----------
    `matrix: List[List[Optional[Piece]]]`
        Matrix of pieces on the board
    `kings: dict[Color, King]`
        Dictionary of kings on the board
    
    Operators
    ---------
    `__str__(self) -> str`
        Returns the string representation of the board
    `__repr__(self) -> str`
        Returns the FEN of the board
    `__getitem__(self, pos: Position) -> Optional[Piece]`
        Returns the piece at the given position
    `__setitem__(self, pos: Position, piece: Piece) -> None`
        Sets the piece at the given position
    `__delitem__(self, pos: Position) -> None`
        Deletes the piece at the given position
    `__contains__(self, piece: Piece) -> bool`
        Returns True if the piece is on the board
    `__iter__(self) -> Generator[Optional[Piece], None, None]`
        Returns an iterator over the pieces on the board
    `__len__(self) -> int`
        Returns the number of pieces on the board
    
    Methods
    -------
    `from_fen(cls, fen: str, pieces_from_fen: dict[str, Type[Piece]]) -> Self`
        Create a board from a FEN string
    `load_fen(self, fen: str, pieces_from_fen: dict[str, Type[Piece]]) -> None`
        Load a FEN string into the board
    `get_king(self, color: Color) -> King`
        Get the king of a color
    `move(self, piece: Piece, pos: Position) -> None`
        Move a piece to a position
    `is_attacked(self, pos: Position, color: Color) -> bool`
        Returns True if the position is attacked by a piece of the given color
    `undo(self) -> None`
        Undo the last move
    `redo(self) -> None`
        Redo the last move
    '''

    matrix: List[List[Optional[Piece]]] = field(init = False, default_factory = lambda: [[None] * 8 for _ in range(8)])
    kings: dict[Color, King] = field(init = False, default_factory = dict)
    en_passant: Optional[Position] = field(init = False, default = None)
    
    @classmethod
    def from_fen(cls, fen: str, pieces_from_fen: dict[str, Type[Piece]]) -> Self:
        '''
        Create a board from a FEN string

        Parameters
        ----------
        `fen: str`
            FEN string
        `pieces_from_fen: dict[str, Type[Piece]]`
            Dictionary of pieces to create from the FEN string
        
        Returns
        -------
        `Board`
            Board created from the FEN string
        '''

        board = cls()
        board.load_fen(fen, pieces_from_fen)
        return board
    
    def load_fen(self, fen: str, pieces_from_fen: dict[str, Type[Piece]]) -> None:
        '''
        Load a FEN string into the board

        Parameters
        ----------
        `fen: str`
            FEN string
        `pieces_from_fen: dict[str, Type[Piece]]`
            Dictionary of pieces to create from the FEN string

        Returns
        -------
        `None`
        '''

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

                self.kings.update({piece.color: piece}) if isinstance(piece, King) else -1
                
                i_col += 1
            
            i_row -= 1

    def __str__(self) -> str:
        border: str = '  +---+---+---+---+---+---+---+---+\n'
        rank_labels: str = '    a   b   c   d   e   f   g   h\n'
        return border + border.join(
                f'{8 - i} | ' + ' | '.join(SPECIAL_CHARS[str(piece)] if piece is not None else ' ' for piece in row) + ' |\n'
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
        return piece in reduce(lambda pieces, row: pieces + row, self.matrix, [])

    def __len__(self) -> int:
        return sum(reduce(lambda sum, element: sum + 1, filter(lambda p: p, pieces), 0) for pieces in self.matrix)

    def get_king(self, color: Color) -> King:
        '''
        Get the king of a color

        Parameters
        ----------
        `color: Color`
            Color of the king to get
        
        Returns
        -------
        `King`
            King of the color
        '''

        return self.kings[color]

    def move(self, piece: Piece, pos: Position) -> None:
        '''
        Move a piece to a position

        Parameters
        ----------
        `piece: Piece`
            Piece to move
        `pos: Position`
            Position to move the piece to
        
        Raises
        ------
        `ValueError`
            If cannot castle (The rook is not in the right place BUG)
        
        Returns
        -------
        `None`
        '''

        if isinstance(piece, King) and abs(piece.pos.diff(pos)[0]) == 2:
            rook = self[pos + (1, 0)] if pos.col == 'g' else self[pos - (2, 0)]
            castle_pos = Position('f' if pos.col == 'g' else 'd', pos.row)

            if isinstance(rook, Rook) and rook.color == piece.color:
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

    def is_attacked(self, pos: Position, color: Color) -> bool:
        '''
        Check if a position is attacked by a color

        Parameters
        ----------
        `pos: Position`
            Position to check
        `color: Color`
            Color to check
        
        Returns
        -------
        `bool`
            Whether the position is attacked by the color
        '''
        
        for piece in self:
            if piece and piece.color == color and (
                piece.can_capture(pos) if isinstance(piece, Pawn) else piece.can_move(self, pos)
            ):
                return True
        return False

    def undo(self) -> None: #! TODO: Implement
        '''
        Undo the last move
        '''

    def redo(self) -> None: #! TODO: Implement
        '''
        Redo the last move
        '''


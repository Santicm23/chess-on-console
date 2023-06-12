
from dataclasses import dataclass, field
from typing import Type, Optional

from ..piece import Piece, Board
from ...helpers.constants import Color, Position
from ...helpers.functions import col_to_int


@dataclass(slots=True)
class Pawn(Piece):
    '''Pawn piece'''
    
    def can_move(self, board: Board, pos: Position) -> bool:
        super(Pawn, self).can_move(board, pos)
        sqr = board[pos]

        match (self.color):

            case Color.WHITE:

                if sqr is None:
                    return self.pos + (0, 1) == pos or (
                        self.pos + (0, 2) == pos and self.pos.row == 2 and board[self.pos + (0, 1)] is None
                    )
                elif sqr.color == Color.BLACK:
                    return self.pos + (1, 1) == pos or self.pos + (-1, 1) == pos
                
            case Color.BLACK:

                if sqr is None:
                    return self.pos + (0, -1) == pos or (
                        self.pos + (0, -2) == pos and self.pos.row == 7 and board[self.pos + (0, -1)] is None
                    )
                elif sqr.color == Color.WHITE:
                    return self.pos + (1, -1) == pos or self.pos + (-1, -1) == pos
        
        return False

    def promote(self, piece_type: Type[Piece]) -> None:
        self.__class__ = piece_type


@dataclass(slots=True)
class Knight(Piece):
    '''Knight piece'''

    def __str__(self) -> str:
        return 'N' if self.color == Color.WHITE else 'n'
    
    def can_move(self, board: Board, pos: Position) -> bool:
        super(Knight, self).can_move(board, pos)

        x, y = self.pos
        new_x, new_y = pos

        x = col_to_int(x)
        new_x = col_to_int(new_x)

        sqr = board[pos]

        if (new_x, new_y) in [(x + 1, y + 2), (x + 2, y + 1), (x + 2, y - 1), (x + 1, y - 2),
                              (x - 1, y - 2), (x - 2, y - 1), (x - 2, y + 1), (x - 1, y + 2)]:
            return sqr is None or sqr.color != self.color
        
        return False


@dataclass(slots=True)
class Bishop(Piece):
    '''Bishop piece'''

    def can_move(self, board: Board, pos: Position) -> bool:
        super(Bishop, self).can_move(board, pos)
        x, y = pos.diff(self.pos)
        
        return abs(x) == abs(y) and self.check_path(board, pos)
    
    def check_path(self, board: Board, pos: Position) -> bool:
        x, y = pos.diff(self.pos)

        cx = 1 if x > 0 else -1
        cy = 1 if y > 0 else -1

        for i in range(1, abs(x)):
            if board[self.pos + (i * cx, i * cy)] is not None:
                return False
        
        sqr = board[pos]

        return sqr is None or sqr.color != self.color



@dataclass(slots=True)
class Rook(Piece):
    '''Rook piece'''

    def can_move(self, board: Board, pos: Position) -> bool:
        super(Rook, self).can_move(board, pos)

        x, y = pos.diff(self.pos)

        return (x == 0 or y == 0) and self.check_path(board, pos)
    
    def check_path(self, board: Board, pos: Position) -> bool:
        x, y = pos.diff(self.pos)

        cx = 1 if x > 0 else (-1 if x < 0 else 0)
        cy = 1 if y > 0 else (-1 if y < 0 else 0)

        for i in range(1, abs(x)):
            if board[self.pos + (i * cx, i * cy)] is not None:
                return False
        for i in range(1, abs(y)):
            if board[self.pos + (i * cx, i * cy)] is not None:
                return False
        
        sqr = board[pos]

        return sqr is None or sqr.color != self.color


@dataclass(slots=True)
class Queen(Piece):
    '''Queen piece'''

    def can_move(self, board: Board, pos: Position) -> bool:
        super(Queen, self).can_move(board, pos)

        x, y = pos.diff(self.pos)

        return (x == 0 or y == 0 or abs(x) == abs(y)) and self.check_path(board, pos)
    
    def check_path(self, board: Board, pos: Position) -> bool:
        x, y = pos.diff(self.pos)

        cx = 1 if x > 0 else (-1 if x < 0 else 0)
        cy = 1 if y > 0 else (-1 if y < 0 else 0)

        for i in range(1, abs(x)):
            if board[self.pos + (i * cx, i * cy)] is not None:
                return False
        for i in range(1, abs(y)):
            if board[self.pos + (i * cx, i * cy)] is not None:
                return False
        
        sqr = board[pos]

        return sqr is None or sqr.color != self.color


@dataclass(slots=True)
class King(Piece):
    '''King piece'''

    def can_move(self, board: Board, pos: Position) -> bool:
        x, y = pos.diff(self.pos)

        sqr = board[pos]

        return super(King, self).can_move(board, pos) and (
            abs(x) <= 1 and abs(y) <= 1 and (sqr is None or sqr.color != self.color) or (
                (str(pos) == 'g1' or str(pos) == 'g8') and self.can_castle(board, 'O-O')
            ) or (
                (str(pos) == 'c1' or str(pos) == 'c8') and self.can_castle(board, 'O-O-O')
            )
        )

    def can_castle(self, board: Board, castle_type: str) -> bool: #Todo: check if in check or passing through check and if he can castle in chess960 mode
        rook: Rook
        piece: Optional[Piece]
        if castle_type == 'O-O':
            piece = board[self.pos + (3, 0)]
        elif castle_type == 'O-O-O':
            piece = board[self.pos + (-4, 0)]
        else:
            return False
        
        if piece is None or not isinstance(piece, Rook):
            return False
        
        rook = piece
        
        x = self.pos.col
        rook_x = rook.pos.col

        x = col_to_int(x)
        rook_x = col_to_int(rook_x)

        if rook_x < x:
            for i in range(1, 4):
                if board[self.pos - (i, 0)] is not None and not isinstance(board[self.pos - (i, 0)], King):
                    return False
        else:
            for i in range(1, 3):
                if board[self.pos + (i, 0)] is not None and not isinstance(board[self.pos + (i, 0)], King):
                    return False
        
        return True

    def castle(self, rook: Rook) -> None:
        x = self.pos.col
        rook_x = rook.pos.col

        x = col_to_int(x)
        rook_x = col_to_int(rook_x)

        if rook_x < x:
            self.move(self.pos - (2, 0))
            rook.move(self.pos - (1, 0))
        else:
            self.move(self.pos + (2, 0))
            rook.move(self.pos + (1, 0))


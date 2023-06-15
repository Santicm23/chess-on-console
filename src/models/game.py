
import re
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Optional, Type, Generator, Callable

from .board import Board
from .piece import Piece
from .pieces.standard import King, Pawn
from ..helpers.constants import Position, Color


@dataclass(slots=True)
class Game(ABC):
    '''
    The Game class is an abstract class that represents a game.
        - It requires the implementation of the update_legal_moves and move methods.
        - The constructor receives the FEN of the starting position as parameter.

    Attributes
    ----------
    `start_fen: str`
        The FEN of the starting position
    `board: Board`
        The board
    `turn: str`
        The turn ('w' or 'b')
    `castling: str`
        The castling rights
    `en_passant: str`
        The en passant square
    `halfmove_clock: int`
        The halfmove clock
    `fullmove_number: int`
        The fullmove number
    `pieces_from_fen: dict[str, Type[Piece]]`
        A dictionary that maps the FEN of a piece to the piece class
    
    Operators
    ---------
    `__str__(self) -> str`
        Returns the string representation of the board
    `__repr__(self) -> str`
        Returns the FEN of the actual position
    `__getitem__(self, pos: str) -> Optional[Piece]`
        Returns the piece at the given position
    `__setitem__(self, pos: str, piece: Piece) -> None`
        Sets the piece at the given position
    `__delitem__(self, pos: str) -> None`
        Deletes the piece at the given position
    `__contains__(self, piece: Piece) -> bool`
        Returns True if the piece is on the board
    `__iter__(self) -> Generator[Optional[Piece], None, None]`
        Returns an iterator over the pieces on the board
    `__len__(self) -> int`
        Returns the number of pieces on the board

    Methods
    -------
    `change_turn() -> None`
        Changes the turn
    `parse_move(move: str) -> tuple[Piece, Position, Optional[Piece], Optional[Type[Piece]]]`
        Parses a move and returns the piece, start position, captured piece and promotion piece
    `undo() -> None`
        Undoes the last move
    `redo() -> None`
        Redoes the last undone move
    `is_check() -> bool`
        Returns True if the king of the player whose turn it is is in check
    `update_legal_moves() -> None`
        Updates the legal moves of all the pieces
    `move(move: str) -> None`
        Moves a piece
    '''

    start_fen: str = field(init = True)
    board: Board = field(init = False)
    turn: str = field(init = False)
    castling: str = field(init = False)
    en_passant: str = field(init = False)
    halfmove_clock: int = field(init = False)
    fullmove_number: int = field(init = False)
    pieces_from_fen: dict[str, Type[Piece]] = field(init = False, default_factory = lambda: {'k': King})

    def __post_init__(self) -> None:
        pass

    def __str__(self) -> str:
        return str(self.board)

    def __repr__(self) -> str:
        return f'{repr(self.board)} {self.turn} {self.castling} {self.en_passant} {self.halfmove_clock} {self.fullmove_number}'

    def __getitem__(self, pos: str) -> Optional[Piece]:
        return self.board[pos]

    def __setitem__(self, pos: str, piece: Piece) -> None:
        self.board[pos] = piece

    def __delitem__(self, pos: str) -> None:
        del self.board[pos]

    def __contains__(self, piece: Piece) -> bool:
        return piece in self.board
    
    def __iter__(self) -> Generator[Optional[Piece], None, None]:
        return iter(self.board)
    
    def __len__(self) -> int:
        return len(self.board)
    
    def change_turn(self) -> None:
        '''
        Changes the turn
        '''

        self.turn = 'w' if self.turn == 'b' else 'b'

    def parse_move(self, move: str) -> tuple[Piece, Position, Optional[Piece], Optional[Type[Piece]]]:
        '''
        Parses a move and returns the piece, start position, captured piece and promotion piece
        
        Parameters
        ----------
        `move: str`
            The move to parse
        
        Raises
        ------
        `ValueError`
            If the move is invalid
        
        Returns
        -------
        `tuple[Piece, Position, Optional[Piece], Optional[Type[Piece]]]`
            The piece, start position, captured piece and promotion piece
        '''

        if not re.match(
            r'^([NBRQK]?[a-h]?[1-8]?x?[a-h][1-8](=[NBRQ])?|O(-O){1,2})$',
            move
        ):
            raise ValueError('Invalid move')
        
        piece: Optional[Piece] = None
        pos: Position
        captured_piece: Optional[Piece] = None
        promotion_piece: Optional[Type[Piece]] = None

        color = Color.WHITE if self.turn == 'w' else Color.BLACK
        
        if move[0] == 'O':
            piece = self.board.get_king(color)
            castle_char: str
            
            col = 'g' if move == 'O-O' else 'c'
            row = 1 if self.turn == 'w' else 8

            castle_char = 'k' if move == 'O-O' else 'q'
            castle_char = castle_char.upper() if self.turn == 'w' else castle_char.lower()

            if not castle_char in self.castling or not piece.can_castle(self.board, move) or self.is_check():
                raise ValueError('Invalid move')
            
            pos = Position(col, row)
        
        else:
            pos_index: int #? Index of the move's position in the string
            if '=' in move:
                if move[0] in 'NBRQK':
                    raise ValueError('Invalid move')
                
                promotion_piece = self.pieces_from_fen[move[-1].lower()]
                pos = Position(move[-4], int(move[-3]))

                pos_index = len(move) - 4
            else:
                pos = Position(move[-2], int(move[-1]))
                pos_index = len(move) - 2
            
            if move[0] not in 'NBRQK':
                move = 'P' + move
                pos_index += 1
            
            condicion: Callable[[Position], bool] = lambda _: True
            
            if pos_index != 1:
                if move[1] in 'abcdefgh':
                    condicion = lambda pos: pos.col == move[1]
                    if move[2] in '12345678':
                        condicion = lambda pos: pos.col == move[1] and pos.row == int(move[2])
                elif move[1] in '12345678':
                    condicion = lambda pos: pos.row == int(move[1])
                    
            for p in self:
                if p and p.color == color and str(p).upper() == move[0] and (
                    condicion(p.pos) and p.is_legal_move(pos)
                ):
                    piece = p
                    break
            
            if isinstance(piece, Pawn) and pos == self.en_passant:
                captured_piece = self[pos.col + ('5' if self.turn == 'w' else '4')]
            else:
                captured_piece = self[str(pos)]
            
            if 'x' in move and not captured_piece:
                raise ValueError('Invalid move')
            elif 'x' not in move and captured_piece:
                raise ValueError('Invalid move')
        
        if not piece:
            raise ValueError('Invalid move')
        
        return piece, pos, captured_piece, promotion_piece

    def undo(self) -> None:
        '''
        Undoes the last move
        '''

        self.board.undo()
    
    def redo(self) -> None:
        '''
        Redoes the last undone move
        '''

        self.board.redo()

    @abstractmethod
    def is_check(self) -> bool:
        '''
        Returns whether the current player is in check or not
        '''

    @abstractmethod
    def update_legal_moves(self) -> None:
        '''
        Updates the legal moves of all the pieces
        '''

    @abstractmethod
    def move(self, move: str) -> None:
        '''
        Moves a piece
        
        Parameters
        ----------
        `move: str`
            The move to make
        '''


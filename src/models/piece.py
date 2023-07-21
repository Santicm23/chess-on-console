'''./src/models/piece.py'''

from __future__ import annotations
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Optional, Protocol

from ..helpers.constants import Color, Position


@dataclass(slots= True)
class Board(Protocol):
    '''
    Board interface
    
    Attributes
    ----------
    `en_passant: Optional[Position]`
        The position of the en passant square
    
    Methods
    -------
    `__getitem__(pos: str | Position) -> Optional[Piece]`
        Returns the piece at the given position.
    `is_valid(pos: Position) -> bool`
        Returns True if the position is valid.
    `is_attacked(pos: Position, color: Color) -> bool`
        Returns True if the position is attacked by a piece of the given color.
    '''

    en_passant: Optional[Position] = field(init= False)

    def __getitem__(self, pos: str | Position) -> Optional[Piece]:...

    def is_valid(self, pos: Position) -> bool:...# pylint: disable=missing-function-docstring

    def is_attacked(self, pos: Position, color: Color) -> bool:...# pylint: disable=missing-function-docstring

@dataclass(slots= True)
class Piece(ABC):
    '''
    Abstract piece class
    
    Attributes
    ----------
    `color: Color`
        The color of the piece
    `pos: Position`
        The position of the piece
    `legal_moves: list[Position]`
        The legal moves of the piece

    Methods
    -------
    `is_legal_move(pos: str | Position) -> bool`
        Returns True if the move is legal.
    `move(pos: Position) -> None`
        Moves the piece to the given position.
    `can_move(board: Board, pos: Position) -> bool`
        Returns True if the piece can move to the given position (not taking into account
        if the move is legal).
    '''

    color: Color
    pos: Position
    legal_moves: list[Position] = field(init= False, default_factory= list)

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return self.__class__.__name__[0].upper()
        # else:
        return self.__class__.__name__[0].lower()

    def is_legal_move(self, pos: str | Position) -> bool:
        '''
        Returns True if the piece can move to the given position.

        Parameters
        ----------
        `pos: str | Position`
            The position to check

        Returns
        -------
        `bool`
            True if the move is legal
        '''

        if isinstance(pos, str) and pos[1].isdigit():
            pos = Position(pos[0], int(pos[1]))
        return pos in self.legal_moves

    def move(self, pos: Position) -> None:
        '''
        Moves the piece to the given position.

        Parameters
        ----------
        `pos: Position`
            The position to move to
        '''

        self.pos = pos

    @abstractmethod
    def can_move(self, board: Board, pos: Position) -> bool:
        '''
        Returns True if the piece can move to the given position.
        
        Parameters
        ----------
        `board: Board`
            The board to check
        `pos: Position`
            The position to check

        Returns
        -------
        `bool`
            True if the piece can move to the given position (not taking into account
            if the move is legal)
        '''

        if self.pos == pos:
            return False
        return True

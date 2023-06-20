
from ..game import Game, GameOver
from ..board import Board
from ..piece import Piece
from ..pieces.standard import Pawn, Knight, Bishop, Rook, Queen, King
from ...helpers.constants import Position, COLOR_MAP, Color, GameOverStatus
from ...helpers.custom_errors import InvalidMoveInputError, InvalidFenError


class StandardGame(Game):
    '''
    The StandardGame class represents a standard chess game.
        - It inherits from the Game class.
        - It implements the update_legal_moves and move methods.
    
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
    `is_check(color: Color) -> bool`
        Returns whether is check or not
    `is_legal(piece: Piece, pos: Position) -> bool`
        Returns whether a move is legal or not
    `update_legal_moves() -> None`
        Updates the legal moves of all the pieces
    `move(move: str) -> None`
        Moves a piece
    '''

    def __init__(self, start_fen: str = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1') -> None:
        super().__init__(start_fen)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.pieces_from_fen.update({
            'p': Pawn, 'n': Knight, 'b': Bishop, 'r': Rook, 'q': Queen, 'k': King
        })

        self.parse_fen(self.start_fen)
    
    def parse_fen(self, fen: str) -> None:
        '''
        Parses a FEN

        Parameters
        ----------
        `fen: str`
            The FEN to parse
        
        Raises
        ------
        `InvalidFenError`
            If the FEN is invalid
        '''

        try:
            fen, turn, castling, en_passant, halfmove_clock, fullmove_number = fen.split()
            self.board = Board.from_fen(fen, self.pieces_from_fen)
            self.turn = turn
            self.castling = castling
            self.en_passant = en_passant
            self.halfmove_clock = int(halfmove_clock)
            self.fullmove_number = int(fullmove_number)
            self.update_legal_moves()

            assert self.turn in 'wb'
            assert self.castling in 'KQkq-'
            assert self.en_passant in '-abcdefgh36'
            assert 0 <= self.halfmove_clock <= 150
            assert 0 <= self.fullmove_number
        except (ValueError, AssertionError, InvalidFenError):
            raise InvalidFenError(fen)
    
    def is_check(self) -> bool:
        '''
        Returns whether is check or not

        Returns
        -------
        `bool`
            Whether the color is in check or not
        '''

        color = COLOR_MAP[self.turn]
        self.change_turn()
        enemy_color = COLOR_MAP[self.turn]

        res: bool = False

        res = self.board.is_attacked(self.board.get_king(color).pos, enemy_color)

        self.change_turn()
        
        return res

    def is_legal(self, piece: Piece, pos: Position) -> bool:
        '''
        Returns whether a move is legal or not

        Parameters
        ----------
        `piece: Piece`
            The piece to move
        `pos: Position`
            The position to move to

        Returns
        -------
        `bool`
            Whether the move is legal or not
        '''

        if not piece.can_move(self.board, pos):
            return False
        
        piece_captured = self.board[pos]
        previous_pos = piece.pos

        self.board.move(piece, pos)

        res = not self.is_check()

        self.board.move(piece, previous_pos)
        self.board[pos] = piece_captured

        return res

    def update_legal_moves(self) -> None:
        '''
        Updates the legal moves of all the pieces
        '''

        for p in self.board.pieces:
            tmp_pos = Position('a', 1)
            if p.color != COLOR_MAP[self.turn]:
                continue

            p.legal_moves.clear()

            for _ in range(64):
                if self.is_legal(p, tmp_pos):
                    p.legal_moves.append(tmp_pos)
                
                try:
                    tmp_pos = next(tmp_pos)
                except StopIteration:
                    break

    def move(self, move: str) -> None:
        '''
        Moves a piece

        Parameters
        ----------
        `move: str`
            The move to make
        
        Raises
        ------
        `InvalidMoveInputError`
            If the move is invalid
        `IllegalMoveError`
            If the move is illegal
        `AssertionError`
            If there is an error in parsing the move function BUG
        '''
        
        piece, pos, piece_captured, promotion_type = self.parse_move(move) 
        previous_pos = piece.pos
        en_passant_changed = False
        self.halfmove_clock += 1

        match piece:
            case Pawn():
                self.halfmove_clock = 0
                chr_p = 'P' if piece.color == Color.BLACK else 'p' # pawn of enemy color

                if abs(pos.row - previous_pos.row) == 2 and (
                    str(self.board[pos + (1, 0)]) == chr_p or str(self.board[pos + (-1, 0)]) == chr_p
                ):
                    self.en_passant = pos + (0, -1) if piece.color == Color.WHITE else pos + (0, 1)
                    en_passant_changed = True
                
                elif pos.row == 1 or pos.row == 8:
                    if not promotion_type:
                        raise InvalidMoveInputError('Promotion type not specified')
                    piece.promote(promotion_type)
                    
                elif str(pos) == self.en_passant:
                    if not piece_captured:
                        raise InvalidMoveInputError('En passant capture not possible *BUG*') # BUG
                    del self.board[piece_captured.pos]
                
            case King():
                if piece.color == Color.WHITE:
                    self.castling = self.castling.replace('K', '').replace('Q', '')
                else:
                    self.castling = self.castling.replace('k', '').replace('q', '')
            
            case Rook():
                if previous_pos == Position('a', 1):
                    self.castling = self.castling.replace('Q', '')
                elif previous_pos == Position('h', 1):
                    self.castling = self.castling.replace('K', '')
                elif previous_pos == Position('a', 8):
                    self.castling = self.castling.replace('q', '')
                elif previous_pos == Position('h', 8):
                    self.castling = self.castling.replace('k', '')
            
            case _:
                pass
        
        if not en_passant_changed:
            self.board.en_passant = None
            self.en_passant = None
        
        self.board.move(piece, pos)
        
        if piece_captured:
            self.halfmove_clock = 0

        if self.castling == '':
            self.castling = '-'

        self.change_turn()
        if self.turn == 'w':
            self.fullmove_number += 1
        
        self.update_legal_moves()

        self.move_history.append(repr(self.board) + self.turn + self.castling + self.en_passant)

        self.game_over() # check if the game is over

    def game_over(self) -> None:
        '''
        Verifies if the game is over

        Raises
        ------
        `GameOver`
            If the game is over
        '''

        if not self.legal_moves:
            if self.is_check():
                self.change_turn()
                raise GameOver(GameOverStatus.CHECKMATE, COLOR_MAP[self.turn])
            else:
                raise GameOver(GameOverStatus.STALEMATE)
        if self.halfmove_clock >= 100:
            raise GameOver(GameOverStatus.FIFTY_MOVE_RULE)
        if self.board.is_triple_repetition():
            raise GameOver(GameOverStatus.THREEFOLD_REPETITION)
        if self.board.is_insufficient_material():
            raise GameOver(GameOverStatus.INSUFFICIENT_MATERIAL)
        
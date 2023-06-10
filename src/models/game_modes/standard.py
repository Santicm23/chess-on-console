
from ..game import Game
from ...models.board import Board
from ...models.piece import Piece
from ..pieces.standard import Pawn, Knight, Bishop, Rook, Queen, King
from ...helpers.console import get_text_input
from ...helpers.constants import Position, color_map


class StandardGame(Game):
    '''Standard chess game'''

    def __init__(self, start_fen: str = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1') -> None:
        super().__init__(start_fen)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.pieces_from_fen.update({
            'p': Pawn, 'n': Knight, 'b': Bishop, 'r': Rook, 'q': Queen, 'k': King
        })

        fen, self.turn, self.castling, self.en_passant, halfmove_clock, fullmove_number = self.start_fen.split()
        self.board = Board.from_fen(fen, self.pieces_from_fen)
        self.halfmove_clock = int(halfmove_clock)
        self.fullmove_number = int(fullmove_number)
        self.update_legal_moves()
    
    def is_legal(self, piece: Piece, pos: Position) -> bool:
        '''Returns whether a move is legal or not.'''
        if not piece.can_move(self.board, pos):
            return False
        
        piece_captured = self.board[pos]
        previous_pos = piece.pos

        self.board.move(piece, pos)
        self.change_turn()

        color = color_map[self.turn]

        res: bool = True

        for p in self.board:
            if p is not None and p.color == color and p.can_move(self.board, self.board.get_king(color).pos):
                res = False
                break

        self.board.move(piece, previous_pos)
        self.board[pos] = piece_captured
        self.fullmove_number -= 1
        self.change_turn()

        return res

    def update_legal_moves(self) -> None:
        for p in self.board:
            tmp_pos = Position('a', 1)
            if p is None:
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
        move_data = self.parse_move(move) 
        print(move_data)
        self.change_turn()
        get_text_input('Press enter to continue...')


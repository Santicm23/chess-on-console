
from ..game import Game
from ...models.board import Board
from ...models.piece import Piece
from ..pieces.standard import Pawn, Knight, Bishop, Rook, Queen, King
from ...helpers.constants import Position, color_map, Color
from ...helpers.functions import col_to_int


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
        '''Returns whether a move is legal or not'''

        if not piece.can_move(self.board, pos): #Todo: castling
            return False
        
        piece_captured = self.board[pos]
        previous_pos = piece.pos

        enemy_color = color_map[self.turn]

        self.board.move(piece, pos)
        self.change_turn()

        color = color_map[self.turn]

        res: bool = True

        for p in self.board:
            if p is not None and p.color == color and p.can_move(self.board, self.board.get_king(enemy_color).pos):
                res = False
                break

        self.board.move(piece, previous_pos)
        self.board[pos] = piece_captured
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
                    print(f'piece {p}, pos {str(p.pos)}', p.legal_moves)
                    break

    def move(self, move: str) -> None:
        piece, pos, piece_captured, promotion_type = self.parse_move(move) 
        previous_pos = piece.pos
        self.board.move(piece, pos)
        self.en_passant = '-'

        self.halfmove_clock += 1
        match piece:
            case Pawn():
                self.halfmove_clock = 0
                chr_p = 'P' if piece.color == Color.BLACK else 'p' # pawn of enemy color
                if abs(piece.pos.row - previous_pos.row) == 2 and (
                    str(self.board[piece.pos + (1, 0)]) == chr_p or str(self.board[piece.pos + (-1, 0)]) == chr_p
                ):
                    self.en_passant = str(piece.pos + (0, -1) if piece.color == Color.WHITE else piece.pos + (0, 1))
                
            case King():
                if piece.color == Color.WHITE:
                    self.castling = self.castling.replace('K', '').replace('Q', '')
                else:
                    self.castling = self.castling.replace('k', '').replace('q', '')
            
            case Rook():
                if piece.pos == Position('a', 1):
                    self.castling = self.castling.replace('Q', '')
                elif piece.pos == Position('h', 1):
                    self.castling = self.castling.replace('K', '')
                elif piece.pos == Position('a', 8):
                    self.castling = self.castling.replace('q', '')
                elif piece.pos == Position('h', 8):
                    self.castling = self.castling.replace('k', '')
        
        if piece_captured is not None:
            self.halfmove_clock = 0
        

        self.change_turn()
        if self.turn == 'w':
            self.fullmove_number += 1
        
        self.update_legal_moves()


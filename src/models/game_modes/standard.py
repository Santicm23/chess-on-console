
from ..game import Game
from ...helpers.console import clear_playing
from ...models.board import Board
from ..pieces.standard import Pawn, Knight, Bishop, Rook, Queen, King


class StandardGame(Game):
    '''Standard chess game'''

    def __init__(self, start_fen: str = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1') -> None:
        super().__init__(start_fen)

    def __post_init__(self) -> None:
        self.pieces_from_fen.update({
            'p': Pawn, 'n': Knight, 'b': Bishop, 'r': Rook, 'q': Queen, 'k': King
        })

        fen, self.turn, self.castling, self.en_passant, halfmove_clock, fullmove_number = self.start_fen.split()
        self.board = Board.from_fen(fen, self.pieces_from_fen)
        self.halfmove_clock = int(halfmove_clock)
        self.fullmove_number = int(fullmove_number)
    
    def play(self) -> None:
        game_over = False

        while not game_over:
            clear_playing('Standard Chess')

            print(self)
            print(repr(self))

            game_over = True

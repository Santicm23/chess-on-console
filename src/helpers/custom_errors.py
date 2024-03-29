'''./src/helpers/custom_errors.py'''


class IllegalMoveError(Exception):
    '''
    Raised when an illigal move is made.

    Attributes
    ----------
    `move: str`
        The illegal move.
    '''
    
    def __init__(self, move: str):
        self.move = move
        super().__init__(f'The move \'{self.move}\' is illegal')


class InvalidMoveInputError(Exception):
    '''
    Raised when an invalid move input is given.

    Attributes
    ----------
    `input: str`
        The invalid input.
    '''
    
    def __init__(self, input: str):
        self.input = input
        super().__init__(f'The input \'{self.input}\' is invalid')


class InvalidFenError(Exception):
    '''
    Raised when an invalid FEN is given.

    Attributes
    ----------
    `fen: str`
        The invalid FEN.
    '''
    
    def __init__(self, fen: str):
        self.fen = fen
        super().__init__(f'The fen code \'{self.fen}\' is invalid')
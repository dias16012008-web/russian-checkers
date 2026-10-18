import copy
from typing import Optional, List, Tuple
from .pieces import Piece

class Board:
    """Represents the 8x8 checkers board and piece placements."""
    
    ROWS: int = 8
    COLS: int = 8
    
    def __init__(self):
        """Initializes an empty board and calls setup()."""
        # Board is a 2D list. None means empty square.
        # Only dark squares (row + col is odd) will have pieces.
        self.grid: List[List[Optional[Piece]]] = [[None for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.white_left = self.black_left = 12
        self.white_kings = self.black_kings = 0
        self.setup_board()
        
    def setup_board(self) -> None:
        """Places pieces in their starting positions."""
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if (row + col) % 2 != 0:
                    if row < 3:
                        self.grid[row][col] = Piece('black')
                    elif row > 4:
                        self.grid[row][col] = Piece('white')

    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        """Gets the piece at a specific position."""
        if 0 <= row < self.ROWS and 0 <= col < self.COLS:
            return self.grid[row][col]
        return None

    def move_piece(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        """Moves a piece from start to end (does not handle capture logic)."""
        sr, sc = start
        er, ec = end
        piece = self.grid[sr][sc]
        self.grid[sr][sc] = None
        self.grid[er][ec] = piece

    def remove_piece(self, row: int, col: int) -> None:
        """Removes a piece from the board and updates counters."""
        piece = self.grid[row][col]
        if piece is not None:
            if piece.color == 'white':
                self.white_left -= 1
                if piece.is_king:
                    self.white_kings -= 1
            else:
                self.black_left -= 1
                if piece.is_king:
                    self.black_kings -= 1
            self.grid[row][col] = None

    def promote_to_king(self, row: int, col: int) -> None:
        """Promotes the piece at the given position to a king and updates counters."""
        piece = self.grid[row][col]
        if piece and not piece.is_king:
            piece.promote()
            if piece.color == 'white':
                self.white_kings += 1
            else:
                self.black_kings += 1

    def copy(self) -> 'Board':
        """Creates a copy of the board for AI and undo functionality."""
        new_board = Board()
        new_board.white_left = self.white_left
        new_board.black_left = self.black_left
        new_board.white_kings = self.white_kings
        new_board.black_kings = self.black_kings
        
        # Faster than deepcopy
        for r in range(self.ROWS):
            for c in range(self.COLS):
                piece = self.grid[r][c]
                if piece:
                    new_board.grid[r][c] = Piece(piece.color, piece.is_king)
                else:
                    new_board.grid[r][c] = None
        return new_board

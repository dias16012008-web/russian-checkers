import pygame
from typing import Tuple, List, Optional
from game.board import Board

class Renderer:
    """Handles rendering the game state using pygame."""
    
    # Constants
    WIDTH, HEIGHT = 800, 800
    ROWS, COLS = 8, 8
    SQUARE_SIZE = WIDTH // COLS

    # Colors
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    GRAY = (128, 128, 128)
    DARK_BROWN = (101, 67, 33)
    LIGHT_BROWN = (210, 180, 140)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)

    def __init__(self, win: pygame.Surface):
        self.win = win
        self.font = pygame.font.SysFont('comicsans', 40)
        self.large_font = pygame.font.SysFont('comicsans', 80)

    def draw_squares(self) -> None:
        """Draws the checkerboard squares."""
        self.win.fill(self.DARK_BROWN)
        for row in range(self.ROWS):
            for col in range(row % 2, self.COLS, 2):
                pygame.draw.rect(self.win, self.LIGHT_BROWN, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

    def draw_piece(self, row: int, col: int, color: str, is_king: bool) -> None:
        """Draws a single piece."""
        radius = self.SQUARE_SIZE // 2 - 10
        center = (col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2, row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2)
        
        piece_color = self.WHITE if color == 'white' else self.BLACK
        pygame.draw.circle(self.win, self.GRAY, center, radius + 2) # Shadow/Border
        pygame.draw.circle(self.win, piece_color, center, radius)
        
        if is_king:
            # Draw a crown or just a yellow circle
            pygame.draw.circle(self.win, self.YELLOW, center, radius // 2)

    def draw_board(self, board: Board) -> None:
        """Draws the board and all pieces."""
        self.draw_squares()
        for row in range(board.ROWS):
            for col in range(board.COLS):
                piece = board.grid[row][col]
                if piece:
                    self.draw_piece(row, col, piece.color, piece.is_king)

    def draw_valid_moves(self, moves: List[Tuple[Tuple[int, int], Tuple[int, int], List[Tuple[int, int]]]]) -> None:
        """Highlights squares for valid moves."""
        for move in moves:
            end_pos = move[1]
            r, c = end_pos
            center = (c * self.SQUARE_SIZE + self.SQUARE_SIZE // 2, r * self.SQUARE_SIZE + self.SQUARE_SIZE // 2)
            pygame.draw.circle(self.win, self.BLUE, center, 15)

    def draw_selected_piece(self, pos: Tuple[int, int]) -> None:
        """Highlights the selected piece."""
        r, c = pos
        rect = (c * self.SQUARE_SIZE, r * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE)
        pygame.draw.rect(self.win, self.GREEN, rect, 5)

    def draw_mandatory_pieces(self, pieces: List[Tuple[int, int]]) -> None:
        """Highlights pieces that MUST move (mandatory capture)."""
        for r, c in pieces:
            rect = (c * self.SQUARE_SIZE, r * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE)
            pygame.draw.rect(self.win, self.RED, rect, 5)

    def draw_ui(self, turn: str, white_left: int, black_left: int) -> None:
        """Draws the turn indicator and piece counts."""
        # This will be drawn on a panel, or simply on top of the board for simplicity
        # Let's draw it at the very top or bottom. We need extra space, or just overlay.
        # Overlay for now.
        text = self.font.render(f"Turn: {turn.capitalize()}", 1, self.RED)
        self.win.blit(text, (10, 10))
        
        count_text = self.font.render(f"W: {white_left} | B: {black_left}", 1, self.RED)
        self.win.blit(count_text, (self.WIDTH - count_text.get_width() - 10, 10))

    def draw_game_over(self, winner: str) -> None:
        """Draws the game over message."""
        if winner == 'draw':
            msg = "Draw!"
        else:
            msg = f"{winner.capitalize()} Wins!"
            
        text = self.large_font.render(msg, 1, self.YELLOW)
        bg_rect = pygame.Rect(
            self.WIDTH//2 - text.get_width()//2 - 20, 
            self.HEIGHT//2 - text.get_height()//2 - 20, 
            text.get_width() + 40, 
            text.get_height() + 40
        )
        pygame.draw.rect(self.win, self.BLACK, bg_rect)
        pygame.draw.rect(self.win, self.WHITE, bg_rect, 5)
        self.win.blit(text, (self.WIDTH//2 - text.get_width()//2, self.HEIGHT//2 - text.get_height()//2))

    def draw_menu(self) -> None:
        """Draws a simple start menu."""
        self.win.fill(self.BLACK)
        title = self.large_font.render("Russian Checkers", 1, self.WHITE)
        self.win.blit(title, (self.WIDTH//2 - title.get_width()//2, 100))
        
        options = [
            "1. Player vs Player",
            "2. Player vs AI (Easy)",
            "3. Player vs AI (Medium)",
            "4. Player vs AI (Hard)"
        ]
        
        for i, opt in enumerate(options):
            text = self.font.render(opt, 1, self.GRAY)
            self.win.blit(text, (self.WIDTH//2 - text.get_width()//2, 300 + i * 60))
        
        pygame.display.update()

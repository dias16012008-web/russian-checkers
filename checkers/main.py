import pygame
import sys
from typing import Optional, Tuple
from game.board import Board
from game.rules import Rules
from game.ai import AI
from ui.renderer import Renderer

# Initialize pygame
pygame.init()

# Setup Window
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Russian Checkers')

# FPS
FPS = 60

class Game:
    def __init__(self, win: pygame.Surface):
        self.win = win
        self.renderer = Renderer(win)
        self.reset()

    def reset(self):
        self.board = Board()
        self.turn = 'white'
        self.selected_pos: Optional[Tuple[int, int]] = None
        self.valid_moves = {}
        self.history = [] # For undo: list of boards
        self.moves_without_capture = 0
        self.winner: Optional[str] = None
        self.is_over = False
        self.ai_opponent: Optional[AI] = None
        self._update_valid_moves()

    def _update_valid_moves(self):
        self.valid_moves = Rules.get_all_valid_moves(self.board, self.turn)
        self.is_over, self.winner = Rules.is_game_over(self.board, self.turn, self.moves_without_capture)

    def select(self, row: int, col: int) -> bool:
        if self.selected_pos:
            result = self._move(row, col)
            if not result:
                self.selected_pos = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece and piece.color == self.turn and (row, col) in self.valid_moves:
            self.selected_pos = (row, col)
            return True
        return False

    def _move(self, row: int, col: int) -> bool:
        piece = self.board.get_piece(row, col)
        if self.selected_pos and piece is None:
            # Check if this is a valid move
            for move in self.valid_moves[self.selected_pos]:
                if move[1] == (row, col):
                    self.history.append((self.board.copy(), self.moves_without_capture))
                    
                    self.board.move_piece(self.selected_pos, (row, col))
                    captured = move[2]
                    becomes_king = move[3]
                    for cr, cc in captured:
                        self.board.remove_piece(cr, cc)
                        
                    Rules.check_promotion(self.board, (row, col), becomes_king)
                    
                    moving_piece = self.board.get_piece(row, col)
                    if captured or (moving_piece and not moving_piece.is_king):
                        self.moves_without_capture = 0
                    else:
                        self.moves_without_capture += 1

                    self.change_turn()
                    return True
        return False

    def change_turn(self):
        self.turn = 'black' if self.turn == 'white' else 'white'
        self.selected_pos = None
        self._update_valid_moves()

    def undo(self):
        if self.history:
            self.board, self.moves_without_capture = self.history.pop()
            self.change_turn() # Undo turn
            if self.ai_opponent and self.history: # If playing AI, undo twice
                self.board, self.moves_without_capture = self.history.pop()
                self.change_turn()
            self.is_over = False
            self.winner = None
            self._update_valid_moves()

    def get_row_col_from_mouse(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        x, y = pos
        row = y // self.renderer.SQUARE_SIZE
        col = x // self.renderer.SQUARE_SIZE
        return row, col

    def main_loop(self):
        clock = pygame.time.Clock()
        run = True
        state = "MENU" # MENU, GAME

        while run:
            clock.tick(FPS)
            
            if state == "MENU":
                self.renderer.draw_menu()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            self.reset()
                            state = "GAME"
                        elif event.key == pygame.K_2:
                            self.reset()
                            self.ai_opponent = AI('black', 2)
                            state = "GAME"
                        elif event.key == pygame.K_3:
                            self.reset()
                            self.ai_opponent = AI('black', 4)
                            state = "GAME"
                        elif event.key == pygame.K_4:
                            self.reset()
                            self.ai_opponent = AI('black', 6)
                            state = "GAME"
                        elif event.key == pygame.K_ESCAPE:
                            run = False
            
            elif state == "GAME":
                # AI Turn
                if not self.is_over and self.ai_opponent and self.turn == self.ai_opponent.color:
                    # Small delay for visual effect
                    pygame.time.delay(300)
                    best_move, _ = self.ai_opponent.get_best_move(self.board)
                    if best_move:
                        start, end, captured, becomes_king = best_move
                        self.history.append((self.board.copy(), self.moves_without_capture))
                        self.board.move_piece(start, end)
                        for cr, cc in captured:
                            self.board.remove_piece(cr, cc)
                        Rules.check_promotion(self.board, end, becomes_king)
                        
                        moving_piece = self.board.get_piece(*end)
                        if captured or (moving_piece and not moving_piece.is_king):
                            self.moves_without_capture = 0
                        else:
                            self.moves_without_capture += 1
                        
                        self.change_turn()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            state = "MENU"
                        elif event.key == pygame.K_r:
                            self.reset()
                        elif event.key == pygame.K_u:
                            self.undo()

                    if event.type == pygame.MOUSEBUTTONDOWN and not self.is_over:
                        if not self.ai_opponent or self.turn != self.ai_opponent.color:
                            pos = pygame.mouse.get_pos()
                            row, col = self.get_row_col_from_mouse(pos)
                            self.select(row, col)

                # Rendering
                self.renderer.draw_board(self.board)
                
                if self.selected_pos:
                    self.renderer.draw_selected_piece(self.selected_pos)
                    self.renderer.draw_valid_moves(self.valid_moves.get(self.selected_pos, []))
                else:
                    mandatory = list(self.valid_moves.keys())
                    if mandatory:
                        # Check if these are actually captures
                        first_moves = self.valid_moves[mandatory[0]]
                        if first_moves and first_moves[0][2]:
                            self.renderer.draw_mandatory_pieces(mandatory)

                self.renderer.draw_ui(self.turn, self.board.white_left, self.board.black_left)

                if self.is_over:
                    self.renderer.draw_game_over(self.winner)

                pygame.display.update()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game(WIN)
    game.main_loop()

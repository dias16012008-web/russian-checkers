from typing import Tuple, List, Optional
import math
from .board import Board
from .rules import Rules

class AI:
    """Minimax AI with alpha-beta pruning."""

    def __init__(self, color: str, depth: int):
        self.color = color
        self.depth = depth

    def evaluate(self, board: Board) -> float:
        """
        Evaluates the board state.
        Positive score favors white, negative score favors black.
        Weights: Regular piece = 10, King = 30.
        Small bonus for advancement towards promotion line.
        """
        score = 0.0
        for r in range(board.ROWS):
            for c in range(board.COLS):
                piece = board.grid[r][c]
                if piece:
                    # Base value
                    value = 30 if piece.is_king else 10
                    
                    # Advancement bonus for regular pieces
                    if not piece.is_king:
                        if piece.color == 'white':
                            advancement = (board.ROWS - 1 - r) * 0.1
                        else:
                            advancement = r * 0.1
                        value += advancement
                        
                    if piece.color == 'white':
                        score += value
                    else:
                        score -= value
        return score

    def get_best_move(self, board: Board) -> Tuple[Optional[Tuple[Tuple[int, int], Tuple[int, int], List[Tuple[int, int]], bool]], float]:
        """Finds the best move using minimax with alpha-beta pruning."""
        is_maximizing = self.color == 'white'
        best_move, score = self.minimax(board, self.depth, -math.inf, math.inf, is_maximizing, 0)
        return best_move, score

    def minimax(self, board: Board, depth: int, alpha: float, beta: float, is_maximizing: bool, moves_without_capture: int) -> Tuple[Optional[Tuple[Tuple[int, int], Tuple[int, int], List[Tuple[int, int]], bool]], float]:
        """Minimax algorithm implementation."""
        turn_color = 'white' if is_maximizing else 'black'
        is_over, winner = Rules.is_game_over(board, turn_color, moves_without_capture)
        
        if is_over:
            if winner == 'white':
                return None, math.inf
            elif winner == 'black':
                return None, -math.inf
            else:
                return None, 0.0

        if depth == 0:
            return None, self.evaluate(board)

        valid_moves = Rules.get_all_valid_moves(board, turn_color)
        
        if not valid_moves:
             return None, -math.inf if is_maximizing else math.inf

        best_move = None
        
        if is_maximizing:
            max_eval = -math.inf
            for start_pos, moves in valid_moves.items():
                for move in moves:
                    end_pos, captured, becomes_king = move[1], move[2], move[3]
                    
                    # Simulate move
                    new_board = board.copy()
                    new_board.move_piece(start_pos, end_pos)
                    for cr, cc in captured:
                        new_board.remove_piece(cr, cc)
                    Rules.check_promotion(new_board, end_pos, becomes_king)
                    
                    moving_piece = new_board.get_piece(*end_pos)
                    if captured or (moving_piece and not moving_piece.is_king):
                        new_moves_without_capture = 0
                    else:
                        new_moves_without_capture = moves_without_capture + 1
                    
                    # Recurse
                    _, evaluation = self.minimax(new_board, depth - 1, alpha, beta, False, new_moves_without_capture)
                    
                    if evaluation > max_eval:
                        max_eval = evaluation
                        best_move = move
                    alpha = max(alpha, evaluation)
                    if beta <= alpha:
                        break # Beta cutoff
                if beta <= alpha:
                    break
            return best_move, max_eval
        else:
            min_eval = math.inf
            for start_pos, moves in valid_moves.items():
                for move in moves:
                    end_pos, captured, becomes_king = move[1], move[2], move[3]
                    
                    # Simulate move
                    new_board = board.copy()
                    new_board.move_piece(start_pos, end_pos)
                    for cr, cc in captured:
                        new_board.remove_piece(cr, cc)
                    Rules.check_promotion(new_board, end_pos, becomes_king)
                    
                    moving_piece = new_board.get_piece(*end_pos)
                    if captured or (moving_piece and not moving_piece.is_king):
                        new_moves_without_capture = 0
                    else:
                        new_moves_without_capture = moves_without_capture + 1
                    
                    # Recurse
                    _, evaluation = self.minimax(new_board, depth - 1, alpha, beta, True, new_moves_without_capture)
                    
                    if evaluation < min_eval:
                        min_eval = evaluation
                        best_move = move
                    beta = min(beta, evaluation)
                    if beta <= alpha:
                        break # Alpha cutoff
                if beta <= alpha:
                    break
            return best_move, min_eval

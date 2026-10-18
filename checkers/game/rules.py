from typing import List, Tuple, Dict, Optional, Set
from .board import Board
from .pieces import Piece

MoveType = Tuple[Tuple[int, int], Tuple[int, int], List[Tuple[int, int]], bool]
# A move is (start_pos, end_pos, list_of_captured_pieces, becomes_king)

class Rules:
    """Handles game logic: move generation, captures, and win conditions."""

    DIRECTIONS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    @staticmethod
    def get_all_valid_moves(board: Board, turn_color: str) -> Dict[Tuple[int, int], List[MoveType]]:
        """
        Gets all valid moves for a given player.
        Mandatory capture rules apply.
        """
        moves: Dict[Tuple[int, int], List[MoveType]] = {}
        has_capture = False

        for row in range(board.ROWS):
            for col in range(board.COLS):
                piece = board.get_piece(row, col)
                if piece and piece.color == turn_color:
                    piece_moves = Rules.get_valid_moves_for_piece(board, (row, col))
                    
                    # Check if these moves include captures
                    captures = [m for m in piece_moves if m[2]]
                    
                    if captures:
                        if not has_capture:
                            # Found the first capture, discard all previously found non-captures
                            moves = {}
                            has_capture = True
                        moves[(row, col)] = captures
                    elif not has_capture and piece_moves:
                        moves[(row, col)] = piece_moves
                        
        return moves

    @staticmethod
    def check_promotion(board: Board, end_pos: Tuple[int, int], becomes_king: bool) -> None:
        """Checks and applies king promotion if a piece should become a king."""
        row, col = end_pos
        piece = board.get_piece(row, col)
        if piece and not piece.is_king and becomes_king:
            board.promote_to_king(row, col)

    @staticmethod
    def is_game_over(board: Board, turn_color: str, moves_without_capture_or_pawn_move: int) -> Tuple[bool, Optional[str]]:
        """
        Checks if the game is over.
        Returns (is_over, winner_color).
        winner_color is 'white', 'black', 'draw', or None.
        """
        # Draw condition
        if moves_without_capture_or_pawn_move >= 30: # 15 moves per side = 30 plies
            return True, 'draw'

        # Check piece count
        if board.white_left == 0:
            return True, 'black'
        elif board.black_left == 0:
            return True, 'white'

        # Check if current player has any valid moves
        valid_moves = Rules.get_all_valid_moves(board, turn_color)
        if not valid_moves:
            winner = 'black' if turn_color == 'white' else 'white'
            return True, winner

        return False, None

    @staticmethod
    def get_valid_moves_for_piece(board: Board, pos: Tuple[int, int]) -> List[MoveType]:
        """Gets all valid moves for a specific piece."""
        row, col = pos
        piece = board.get_piece(row, col)
        if not piece:
            return []

        moves: List[MoveType] = []
        captures: List[MoveType] = []
        
        # Start exploring captures
        captures = Rules._get_captures(board, pos, pos, piece, set(), [], piece.is_king)
        
        # If there are captures, we MUST take them, so don't even calculate simple moves
        if captures:
            return captures

        # If no captures, calculate simple moves
        if piece.is_king:
            moves = Rules._get_king_simple_moves(board, pos)
        else:
            moves = Rules._get_man_simple_moves(board, pos, piece.color)

        return moves

    @staticmethod
    def _get_captures(
        board: Board, 
        start_pos: Tuple[int, int], 
        current_pos: Tuple[int, int], 
        piece: Piece, 
        captured_so_far: Set[Tuple[int, int]],
        capture_path: List[Tuple[int, int]],
        is_king: bool
    ) -> List[MoveType]:
        """
        Recursively finds all possible capture sequences (multi-jumps).
        captured_so_far: set of coordinates of pieces already captured in this sequence.
        capture_path: ordered list of coordinates of pieces captured.
        is_king: whether the piece is acting as a king (can be promoted during sequence).
        """
        row, col = current_pos
        captures: List[MoveType] = []

        if is_king:
            # King capture logic
            for dr, dc in Rules.DIRECTIONS:
                r, c = row + dr, col + dc
                piece_to_capture = None
                cap_r, cap_c = -1, -1
                
                # Move along diagonal looking for a piece to jump over
                while 0 <= r < board.ROWS and 0 <= c < board.COLS:
                    p = board.get_piece(r, c)
                    if p is not None:
                        if (r, c) in captured_so_far or p.color == piece.color:
                            break # Blocked by own piece or already captured piece
                        else:
                            piece_to_capture = p
                            cap_r, cap_c = r, c
                            r += dr
                            c += dc
                            break # Found a piece to potentially jump
                    r += dr
                    c += dc
                
                if piece_to_capture:
                    # Now check valid landing spots after the captured piece
                    landing_spots = []
                    while 0 <= r < board.ROWS and 0 <= c < board.COLS:
                        p = board.get_piece(r, c)
                        if p is None or (r, c) == start_pos:
                            landing_spots.append((r, c))
                        else:
                            break # Blocked
                        r += dr
                        c += dc
                    
                    for land_r, land_c in landing_spots:
                        new_captured_set = set(captured_so_far)
                        new_captured_set.add((cap_r, cap_c))
                        new_capture_path = list(capture_path)
                        new_capture_path.append((cap_r, cap_c))
                        
                        # Temporarily move to landing spot to check for multi-jumps
                        further_captures = Rules._get_captures(
                            board, start_pos, (land_r, land_c), piece, new_captured_set, new_capture_path, is_king
                        )
                        
                        if further_captures:
                            captures.extend(further_captures)
                        else:
                            captures.append((start_pos, (land_r, land_c), new_capture_path, True))
                            
        else:
            # Regular piece capture logic
            for dr, dc in Rules.DIRECTIONS:
                cap_r, cap_c = row + dr, col + dc
                land_r, land_c = row + 2 * dr, col + 2 * dc
                
                if 0 <= land_r < board.ROWS and 0 <= land_c < board.COLS:
                    cap_piece = board.get_piece(cap_r, cap_c)
                    land_piece = board.get_piece(land_r, land_c)
                    
                    if cap_piece and cap_piece.color != piece.color and (cap_r, cap_c) not in captured_so_far:
                        if land_piece is None or (land_r, land_c) == start_pos:
                            new_captured_set = set(captured_so_far)
                            new_captured_set.add((cap_r, cap_c))
                            new_capture_path = list(capture_path)
                            new_capture_path.append((cap_r, cap_c))
                            
                            # Check promotion during jump
                            promoted = False
                            if not is_king:
                                if (piece.color == 'white' and land_r == 0) or (piece.color == 'black' and land_r == board.ROWS - 1):
                                    promoted = True
                            
                            further_captures = Rules._get_captures(
                                board, start_pos, (land_r, land_c), piece, new_captured_set, new_capture_path, is_king or promoted
                            )
                            
                            if further_captures:
                                captures.extend(further_captures)
                            else:
                                captures.append((start_pos, (land_r, land_c), new_capture_path, is_king or promoted))

        return captures

    @staticmethod
    def _get_man_simple_moves(board: Board, pos: Tuple[int, int], color: str) -> List[MoveType]:
        """Gets simple (non-capture) moves for a regular man."""
        row, col = pos
        moves: List[MoveType] = []
        directions = [(-1, -1), (-1, 1)] if color == 'white' else [(1, -1), (1, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < board.ROWS and 0 <= c < board.COLS:
                if board.get_piece(r, c) is None:
                    promoted = (color == 'white' and r == 0) or (color == 'black' and r == board.ROWS - 1)
                    moves.append((pos, (r, c), [], promoted))
        return moves

    @staticmethod
    def _get_king_simple_moves(board: Board, pos: Tuple[int, int]) -> List[MoveType]:
        """Gets simple (non-capture) moves for a flying king."""
        row, col = pos
        moves: List[MoveType] = []
        
        for dr, dc in Rules.DIRECTIONS:
            r, c = row + dr, col + dc
            while 0 <= r < board.ROWS and 0 <= c < board.COLS:
                if board.get_piece(r, c) is None:
                    moves.append((pos, (r, c), [], True))
                else:
                    break # Blocked by a piece
                r += dr
                c += dc
        return moves

import pytest
from game.board import Board
from game.pieces import Piece
from game.rules import Rules

def setup_empty_board():
    board = Board()
    board.grid = [[None for _ in range(8)] for _ in range(8)]
    board.white_left = board.black_left = 0
    board.white_kings = board.black_kings = 0
    return board

def test_simple_move():
    board = setup_empty_board()
    board.grid[5][2] = Piece('white')
    board.white_left = 1
    
    moves = Rules.get_all_valid_moves(board, 'white')
    assert (5, 2) in moves
    
    possible_ends = [m[1] for m in moves[(5, 2)]]
    assert (4, 1) in possible_ends
    assert (4, 3) in possible_ends
    assert len(possible_ends) == 2
    assert len(moves[(5, 2)][0][2]) == 0 # no captures

def test_mandatory_capture():
    board = setup_empty_board()
    board.grid[5][2] = Piece('white')
    board.grid[4][3] = Piece('black')
    board.white_left = 1
    board.black_left = 1
    
    moves = Rules.get_all_valid_moves(board, 'white')
    assert (5, 2) in moves
    
    possible_ends = [m[1] for m in moves[(5, 2)]]
    assert (3, 4) in possible_ends
    assert (4, 1) not in possible_ends # simple move should be ignored
    assert len(possible_ends) == 1
    assert (4, 3) in moves[(5, 2)][0][2] # black piece captured

def test_multi_jump():
    board = setup_empty_board()
    board.grid[5][2] = Piece('white')
    board.grid[4][3] = Piece('black')
    board.grid[2][5] = Piece('black')
    board.white_left = 1
    board.black_left = 2
    
    moves = Rules.get_all_valid_moves(board, 'white')
    
    possible_ends = [m[1] for m in moves[(5, 2)]]
    assert (1, 6) in possible_ends
    assert (3, 4) not in possible_ends # must complete multi-jump
    
    captures = moves[(5, 2)][0][2]
    assert (4, 3) in captures
    assert (2, 5) in captures
    assert len(captures) == 2

def test_king_promotion():
    board = setup_empty_board()
    board.grid[1][2] = Piece('white')
    board.white_left = 1
    
    # Simulate move
    Rules.check_promotion(board, (1, 2), False)
    assert not board.grid[1][2].is_king
    
    board.move_piece((1, 2), (0, 3))
    Rules.check_promotion(board, (0, 3), True)
    assert board.grid[0][3].is_king
    assert board.white_kings == 1

def test_flying_king_capture():
    board = setup_empty_board()
    king = Piece('white', is_king=True)
    board.grid[7][0] = king
    board.white_left = 1
    board.white_kings = 1
    
    board.grid[4][3] = Piece('black')
    board.black_left = 1
    
    moves = Rules.get_all_valid_moves(board, 'white')
    
    possible_ends = [m[1] for m in moves[(7, 0)]]
    # Can land anywhere after the piece
    assert (3, 4) in possible_ends
    assert (2, 5) in possible_ends
    assert (1, 6) in possible_ends
    assert (0, 7) in possible_ends
    
    for m in moves[(7, 0)]:
        assert (4, 3) in m[2]

def test_win_detection():
    board = setup_empty_board()
    board.grid[0][1] = Piece('black')
    board.black_left = 1
    
    # White has no pieces
    is_over, winner = Rules.is_game_over(board, 'white', 0)
    assert is_over
    assert winner == 'black'
    
    # Black is blocked
    board.grid[0][1] = Piece('white')
    board.white_left = 1
    board.black_left = 0
    
    board.grid[7][0] = Piece('black')
    board.grid[6][1] = Piece('white')
    # Since black piece is at (7, 0), and moves diagonally...
    # Black wants to move up. The only direction is (6, 1). 
    # If (6, 1) has a white piece, and (5, 2) has a white piece or is off-board...
    # Wait, simple piece at 7,0 cannot move forward (-1, 1). 
    # Actually, simple pieces can capture backwards in Russian draughts.
    # So if there is a white piece at (6, 1), black can capture it by jumping to (5, 2).
    # To completely block black at (7,0), we need to block the capture landing spot too.
    board.grid[5][2] = Piece('white')
    board.black_left = 1
    board.white_left = 3
    
    is_over, winner = Rules.is_game_over(board, 'black', 0)
    assert is_over
    assert winner == 'white'

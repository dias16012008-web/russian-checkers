# Russian Checkers

A complete implementation of Russian draughts (checkers) in Python using pygame.

## Project Structure
```
russian-checkers/
├── main.py            # Entry point, game loop, and menu
├── requirements.txt   # Project dependencies
├── README.md          # Project documentation
├── .gitignore         # Git ignore file
├── pytest.ini         # Pytest configuration
├── game/
│   ├── __init__.py    # Python package marker
│   ├── board.py       # Board state and piece placement
│   ├── pieces.py      # Piece class (color, is_king)
│   ├── rules.py       # Move generation, capture logic, win detection
│   └── ai.py          # Minimax AI with alpha-beta pruning
├── ui/
│   ├── __init__.py    # Python package marker
│   └── renderer.py    # Drawing the board, pieces, highlights using pygame
└── tests/
    ├── __init__.py    # Python package marker
    └── test_rules.py  # Pytest tests for game rules
```

## Features
- Player vs Player mode (hot-seat)
- Player vs Computer mode (Easy, Medium, Hard depths 2, 4, 6 respectively)
- Mandatory captures highlighted in red
- Legal moves highlighted in blue
- Selected piece highlighted in green
- Turn indicators, pieces remaining count, and game over messages
- Undo feature

## Rules of Russian Draughts
- Played on an 8x8 board, pieces only on dark squares.
- 12 pieces per side, white moves first.
- Regular pieces move one square diagonally forward.
- Regular pieces can capture both forward and backward.
- Capturing is mandatory. If several captures are available, the player may choose any, but must complete the full multi-jump sequence.
- A piece that reaches the last row becomes a king. If this happens during a capture, it continues capturing as a king in the same turn.
- Kings move and capture any distance along diagonals ("flying king").
- Captured pieces are removed after the whole move is completed (no jumping over the same piece twice).
- A player loses when they have no pieces or no legal moves.
- Draw occurs when neither side can make progress (e.g. 15 moves with only kings and no captures).

## Step-by-Step Setup

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd russian-checkers
   ```

2. **Create a virtual environment:**
   - On Windows:
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install the requirements:**
   Make sure you have Python 3.10+ installed.
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the game:**
   ```bash
   python main.py
   ```

## Controls
- **Mouse Click:** Select a piece and click on a highlighted square to move.
- **Keys 1-4 (Menu):** Choose game mode.
- **R:** Restart the current game.
- **U:** Undo the last move.
- **Esc:** Return to the main menu from the game, or quit from the main menu.

## Tests
Run unit tests with pytest from the project root directory (`russian-checkers/`):
```bash
pytest
```

## Troubleshooting
- **`pygame` not installed or `ModuleNotFoundError: No module named 'pygame'`**: Ensure your virtual environment is activated and you have run `pip install -r requirements.txt`.
- **Wrong Python version**: This project requires Python 3.10 or higher. You can check your version with `python --version`.
- **`ModuleNotFoundError: No module named 'game'`**: This usually means the script or tests were run from the wrong directory. Ensure you are inside the `russian-checkers` directory when running `python main.py` or `pytest`.

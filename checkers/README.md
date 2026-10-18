# Russian Checkers

A complete implementation of Russian draughts (checkers) in Python using pygame.

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

## Installation

1. Make sure you have Python 3.10+ installed.
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run
Run the main script to start the game:
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
Run unit tests with:
```bash
pytest
```

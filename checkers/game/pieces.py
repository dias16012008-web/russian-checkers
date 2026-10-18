class Piece:
    """Represents a checkers piece on the board."""
    
    def __init__(self, color: str, is_king: bool = False):
        """
        Initializes a piece.
        
        Args:
            color (str): The color of the piece ('white' or 'black').
            is_king (bool): True if the piece is a king, False otherwise.
        """
        self.color = color
        self.is_king = is_king
    
    def promote(self) -> None:
        """Promotes the piece to a king."""
        self.is_king = True

    def __repr__(self) -> str:
        """String representation of the piece."""
        king_str = "King" if self.is_king else "Man"
        return f"{self.color.capitalize()} {king_str}"

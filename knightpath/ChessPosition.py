from typing import Tuple, Optional

class ChessPosition:
    FILES = 'ABCDEFGH'
    RANKS = '12345678'

    def __init__(self, notation: Optional[str] = None, coords: Optional[Tuple[int, int]] = None) -> None:
        if notation:
            self.from_notation(notation)
        elif coords:
            self.from_coords(coords)
        else:
            raise ValueError("Either notation or coords must be provided.")

    def from_notation(self, notation: str) -> None:
        file, rank = notation[0].upper(), notation[1]
        if file not in self.FILES or rank not in self.RANKS:
            raise ValueError(f"Invalid chess notation: {notation}")
        self.x = self.FILES.index(file)
        self.y = self.RANKS.index(rank)

    def from_coords(self, coords: Tuple[int, int]) -> None:
        x, y = coords
        if not (0 <= x < 8) or not (0 <= y < 8):
            raise ValueError(f"Invalid Cartesian coordinates: {coords}")
        self.x = x
        self.y = y

    def to_notation(self) -> str:
        file = self.FILES[self.x]
        rank = self.RANKS[self.y]
        return f"{file}{rank}"

    def to_coords(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def __repr__(self) -> str:
        return f"ChessPosition(notation='{self.to_notation()}', coords={self.to_coords()})"

# Example usage:
position1 = ChessPosition(notation='A5')
print(position1)             # Output: ChessPosition(notation='A5', coords=(0, 4))
print(position1.to_coords()) # Output: (0, 4)

position2 = ChessPosition(coords=(0, 4))
print(position2)             # Output: ChessPosition(notation='A5', coords=(0, 4))
print(position2.to_notation()) # Output: 'A5'

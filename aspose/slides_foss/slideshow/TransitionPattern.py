from __future__ import annotations
from enum import Enum
class TransitionPattern(Enum):
    """Specifies a geometric pattern that tiles together to fill a larger area."""
    DIAMOND = 'Diamond'  # Diamond tile pattern
    HEXAGON = 'Hexagon'  # Hexagon tile pattern

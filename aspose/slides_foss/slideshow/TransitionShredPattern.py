from __future__ import annotations
from enum import Enum
class TransitionShredPattern(Enum):
    """Specifies a geometric shape that tiles together to fill a larger area."""
    STRIP = 'Strip'  # Vertical strips
    RECTANGLE = 'Rectangle'  # Small rectangles

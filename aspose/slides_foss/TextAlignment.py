from __future__ import annotations
from enum import Enum

class TextAlignment(Enum):
    """Represents different text alignment styles."""
    NOT_DEFINED = 'NotDefined'  # Default aligment.
    LEFT = 'Left'  # Left alignment.
    CENTER = 'Center'  # Center alignment.
    RIGHT = 'Right'  # Right alignment.
    JUSTIFY = 'Justify'  # Justify alignment.
    JUSTIFY_LOW = 'JustifyLow'  # Kashida justify low.
    DISTRIBUTED = 'Distributed'  # Distributed alignment.

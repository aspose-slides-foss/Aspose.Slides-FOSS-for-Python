from __future__ import annotations
from enum import Enum


class DisplayBlanksAsType(Enum):
    """Determines how missing data will be displayed."""
    GAP = 'Gap'
    SPAN = 'Span'
    ZERO = 'Zero'

from __future__ import annotations
from enum import Enum

class LineJoinStyle(Enum):
    """Represents the lines join style."""
    NOT_DEFINED = 'NotDefined'
    ROUND = 'Round'
    BEVEL = 'Bevel'
    MITER = 'Miter'

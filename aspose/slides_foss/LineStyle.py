from __future__ import annotations
from enum import Enum

class LineStyle(Enum):
    """Represents the style of a line."""
    NOT_DEFINED = 'NotDefined'
    SINGLE = 'Single'
    THIN_THIN = 'ThinThin'
    THICK_THIN = 'ThickThin'
    THIN_THICK = 'ThinThick'
    THICK_BETWEEN_THIN = 'ThickBetweenThin'

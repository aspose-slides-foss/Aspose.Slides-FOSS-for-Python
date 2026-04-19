from __future__ import annotations
from enum import Enum


class MarkerStyleType(Enum):
    """Determines form of marker on chart's data point."""
    NOT_DEFINED = 'NotDefined'
    CIRCLE = 'Circle'
    DASH = 'Dash'
    DIAMOND = 'Diamond'
    DOT = 'Dot'
    NONE = 'None'
    PICTURE = 'Picture'
    PLUS = 'Plus'
    SQUARE = 'Square'
    STAR = 'Star'
    TRIANGLE = 'Triangle'
    X = 'X'

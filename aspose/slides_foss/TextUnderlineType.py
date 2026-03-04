from __future__ import annotations
from enum import Enum

class TextUnderlineType(Enum):
    """Represents the type of text underline."""
    NOT_DEFINED = 'NotDefined'
    NONE = 'None'
    WORDS = 'Words'
    SINGLE = 'Single'
    DOUBLE = 'Double'
    HEAVY = 'Heavy'
    DOTTED = 'Dotted'
    HEAVY_DOTTED = 'HeavyDotted'
    DASHED = 'Dashed'
    HEAVY_DASHED = 'HeavyDashed'
    LONG_DASHED = 'LongDashed'
    HEAVY_LONG_DASHED = 'HeavyLongDashed'
    DOT_DASH = 'DotDash'
    HEAVY_DOT_DASH = 'HeavyDotDash'
    DOT_DOT_DASH = 'DotDotDash'
    HEAVY_DOT_DOT_DASH = 'HeavyDotDotDash'
    WAVY = 'Wavy'
    HEAVY_WAVY = 'HeavyWavy'
    DOUBLE_WAVY = 'DoubleWavy'

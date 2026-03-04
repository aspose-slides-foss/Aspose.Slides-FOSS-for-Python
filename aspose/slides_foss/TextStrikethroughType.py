from __future__ import annotations
from enum import Enum

class TextStrikethroughType(Enum):
    """Represents the type of text strikethrough."""
    NOT_DEFINED = 'NotDefined'
    NONE = 'None'
    SINGLE = 'Single'
    DOUBLE = 'Double'

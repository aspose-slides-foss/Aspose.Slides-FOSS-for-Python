from __future__ import annotations
from enum import Enum

class TextAnchorType(Enum):
    """text box alignment within a text area."""
    NOT_DEFINED = 'NotDefined'
    TOP = 'Top'
    CENTER = 'Center'
    BOTTOM = 'Bottom'
    JUSTIFIED = 'Justified'
    DISTRIBUTED = 'Distributed'

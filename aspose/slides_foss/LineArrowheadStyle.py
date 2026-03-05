from __future__ import annotations
from enum import Enum

class LineArrowheadStyle(Enum):
    """Represents the style of an arrowhead."""
    NOT_DEFINED = 'NotDefined'
    NONE = 'None'
    TRIANGLE = 'Triangle'
    STEALTH = 'Stealth'
    DIAMOND = 'Diamond'
    OVAL = 'Oval'
    OPEN = 'Open'

from __future__ import annotations
from enum import Enum

class BackgroundType(Enum):
    """Defines the slide background fill source."""
    NOT_DEFINED = 'NotDefined'
    THEMED = 'Themed'
    OWN_BACKGROUND = 'OwnBackground'

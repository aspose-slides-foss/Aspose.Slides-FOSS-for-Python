from __future__ import annotations
from enum import Enum

class BulletType(Enum):
    """Represents the type of the extended bullets."""
    NOT_DEFINED = 'NotDefined'
    NONE = 'None'
    SYMBOL = 'Symbol'  # Sysmbol bullets.
    NUMBERED = 'Numbered'  # Numbered bullets.
    PICTURE = 'Picture'  # Picture bullets.

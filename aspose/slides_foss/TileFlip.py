from __future__ import annotations
from enum import Enum

class TileFlip(Enum):
    """Defines tile flipping mode."""
    NOT_DEFINED = 'NotDefined'
    NO_FLIP = 'NoFlip'
    FLIP_X = 'FlipX'
    FLIP_Y = 'FlipY'
    FLIP_BOTH = 'FlipBoth'

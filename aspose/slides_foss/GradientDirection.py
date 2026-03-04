from __future__ import annotations
from enum import Enum

class GradientDirection(Enum):
    """Represents the gradient style."""
    NOT_DEFINED = 'NotDefined'  # Not defined
    FROM_CORNER1 = 'FromCorner1'  # From Top Left Corner
    FROM_CORNER2 = 'FromCorner2'  # From Top Right Corner
    FROM_CORNER3 = 'FromCorner3'  # From Bottom Left Corner
    FROM_CORNER4 = 'FromCorner4'  # From Bottom Right Corner
    FROM_CENTER = 'FromCenter'  # From Center

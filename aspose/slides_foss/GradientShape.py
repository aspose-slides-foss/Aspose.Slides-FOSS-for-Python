from __future__ import annotations
from enum import Enum

class GradientShape(Enum):
    """Represents the shape of gradient fill."""
    NOT_DEFINED = 'NotDefined'
    LINEAR = 'Linear'
    RECTANGLE = 'Rectangle'
    RADIAL = 'Radial'
    PATH = 'Path'

from __future__ import annotations
from enum import Enum

class BevelPresetType(Enum):
    """Constants which define 3D bevel of shape."""
    NOT_DEFINED = 'NotDefined'
    ANGLE = 'Angle'
    ART_DECO = 'ArtDeco'
    CIRCLE = 'Circle'
    CONVEX = 'Convex'
    COOL_SLANT = 'CoolSlant'
    CROSS = 'Cross'
    DIVOT = 'Divot'
    HARD_EDGE = 'HardEdge'
    RELAXED_INSET = 'RelaxedInset'
    RIBLET = 'Riblet'
    SLOPE = 'Slope'
    SOFT_ROUND = 'SoftRound'

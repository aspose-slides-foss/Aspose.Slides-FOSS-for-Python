from __future__ import annotations
from enum import Enum

class MotionPathPointsType(Enum):
    """Represent types of points in animation motion path."""
    NONE = 'None'
    AUTO = 'Auto'
    CORNER = 'Corner'
    STRAIGHT = 'Straight'
    SMOOTH = 'Smooth'
    CURVE_AUTO = 'CurveAuto'
    CURVE_CORNER = 'CurveCorner'
    CURVE_STRAIGHT = 'CurveStraight'
    CURVE_SMOOTH = 'CurveSmooth'

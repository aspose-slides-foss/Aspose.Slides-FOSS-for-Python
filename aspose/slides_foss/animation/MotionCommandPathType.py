from __future__ import annotations
from enum import Enum

class MotionCommandPathType(Enum):
    """Represent types of command for animation motion effect behavior."""
    MOVE_TO = 'MoveTo'
    LINE_TO = 'LineTo'
    CURVE_TO = 'CurveTo'
    CLOSE_LOOP = 'CloseLoop'
    END = 'End'

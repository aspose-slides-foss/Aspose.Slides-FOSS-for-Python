from __future__ import annotations
from enum import Enum

class LineDashStyle(Enum):
    """Represents the line dash style."""
    NOT_DEFINED = 'NotDefined'
    SOLID = 'Solid'
    DOT = 'Dot'
    DASH = 'Dash'
    LARGE_DASH = 'LargeDash'
    DASH_DOT = 'DashDot'
    LARGE_DASH_DOT = 'LargeDashDot'
    LARGE_DASH_DOT_DOT = 'LargeDashDotDot'
    SYSTEM_DASH = 'SystemDash'
    SYSTEM_DOT = 'SystemDot'
    SYSTEM_DASH_DOT = 'SystemDashDot'
    SYSTEM_DASH_DOT_DOT = 'SystemDashDotDot'
    CUSTOM = 'Custom'

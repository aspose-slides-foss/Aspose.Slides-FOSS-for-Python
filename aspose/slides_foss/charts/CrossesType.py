from __future__ import annotations
from enum import Enum

class CrossesType(Enum):
    """Determines where axis will cross."""
    AXIS_CROSSES_AT_ZERO = 'AxisCrossesAtZero'  # The category axis crosses at the zero point of the value axis (if possible), or the minimum value (if the minimum is greater than zero) or the maximum (if the maximum is less than zero).
    MAXIMUM = 'Maximum'  # The axis crosses at the maximum value.
    CUSTOM = 'Custom'  # Custom value from property CrossAt

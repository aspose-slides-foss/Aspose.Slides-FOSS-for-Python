from __future__ import annotations
from enum import Enum


class TrendlineType(Enum):
    """Represents type of trend line"""
    EXPONENTIAL = 'Exponential'
    LINEAR = 'Linear'
    LOGARITHMIC = 'Logarithmic'
    MOVING_AVERAGE = 'MovingAverage'
    POLYNOMIAL = 'Polynomial'
    POWER = 'Power'

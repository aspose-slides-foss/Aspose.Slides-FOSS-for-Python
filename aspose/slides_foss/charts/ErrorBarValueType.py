from __future__ import annotations
from enum import Enum


class ErrorBarValueType(Enum):
    """Represents type of error bar value"""
    CUSTOM = 'Custom'
    FIXED = 'Fixed'
    PERCENTAGE = 'Percentage'
    STANDARD_DEVIATION = 'StandardDeviation'
    STANDARD_ERROR = 'StandardError'

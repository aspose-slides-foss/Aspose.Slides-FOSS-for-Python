from __future__ import annotations
from enum import Enum


class ErrorBarType(Enum):
    """Represents type of error bar"""
    BOTH = 'Both'
    MINUS = 'Minus'
    PLUS = 'Plus'

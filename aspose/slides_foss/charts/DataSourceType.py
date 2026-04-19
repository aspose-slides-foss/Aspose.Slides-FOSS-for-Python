from __future__ import annotations
from enum import Enum


class DataSourceType(Enum):
    """Data source types."""
    WORKSHEET = 'Worksheet'
    STRING_LITERALS = 'StringLiterals'
    DOUBLE_LITERALS = 'DoubleLiterals'

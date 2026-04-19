from __future__ import annotations
from enum import Enum


class ChartDataSourceType(Enum):
    """Represents a type of data source of the chart."""
    INTERNAL_WORKBOOK = 'InternalWorkbook'
    EXTERNAL_WORKBOOK = 'ExternalWorkbook'

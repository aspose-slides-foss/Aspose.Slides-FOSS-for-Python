from __future__ import annotations
from enum import Enum

class TimeUnitType(Enum):
    """Represents the base unit for the category axis"""
    NONE = 'None'  # Values will displayed as is.
    DAYS = 'Days'  # Specifies the chart data shall be shown in days.
    MONTHS = 'Months'  # Specifies the chart data shall be shown in months.
    YEARS = 'Years'  # Specifies the chart data shall be shown in years.

from __future__ import annotations
from enum import Enum

class DisplayUnitType(Enum):
    """Determines multiplicity of the displayed data."""
    NONE = 'None'  # Values will be displayed as-is.
    HUNDREDS = 'Hundreds'  # Specifies the values on the chart shall be divided by 100.
    THOUSANDS = 'Thousands'  # Specifies the values on the chart shall be divided by 1,000.
    TEN_THOUSANDS = 'TenThousands'  # Specifies the values on the chart shall be divided by 10,000.
    HUNDRED_THOUSANDS = 'HundredThousands'  # Specifies the values on the chart shall be divided by 100,000.
    MILLIONS = 'Millions'  # Specifies the values on the chart shall be divided by 1,000,000.
    TEN_MILLIONS = 'TenMillions'  # Specifies the values on the chart shall be divided by 10,000,000.
    HUNDRED_MILLIONS = 'HundredMillions'  # Specifies the values on the chart shall be divided by 100,000,000.
    BILLIONS = 'Billions'  # Specifies the values on the chart shall be divided by 1,000,000,000.
    TRILLIONS = 'Trillions'  # Specifies the values on the chart shall be divided by 1,000,000,000,000.
    CUSTOM_VALUE = 'CustomValue'  # Specifies the values on the chart shall be divided by a custom value.

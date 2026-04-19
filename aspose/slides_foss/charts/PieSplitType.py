from __future__ import annotations
from enum import Enum

class PieSplitType(Enum):
    """Represents a type of splitting points in the second pie or bar on a pie-of-pie or bar-of-pie chart."""
    DEFAULT = 'Default'  # Specifies the data points shall be split using the default mechanism for this chart type.
    CUSTOM = 'Custom'  # Specifies the data points shall be split between the pie and the second chart according to the Custom Split values.
    BY_PERCENTAGE = 'ByPercentage'  # Specifies the data points shall be split between the pie and the second chart by putting the points with percentage less than Split Position percent in the second chart.
    BY_POS = 'ByPos'  # Specifies the data points shall be split between the pie and the second chart by putting the last Split Position of the data points in the second chart.
    BY_VALUE = 'ByValue'  # Specifies the data points shall be split between the pie and the second chart by putting the data points with value less than Split Position in the second chart.

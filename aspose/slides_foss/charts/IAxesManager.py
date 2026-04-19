from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .IAxis import IAxis

class IAxesManager(ABC):
    """Provides access to chart axes."""
    @property
    def horizontal_axis(self) -> IAxis:
        """Gets the chart's horizontal axis. Read-only ."""
        ...

    @property
    def secondary_horizontal_axis(self) -> IAxis:
        """Gets the chart's secondary horizontal axis. Read-only ."""
        ...

    @property
    def vertical_axis(self) -> IAxis:
        """Gets the chart's vertical axis. Read-only ."""
        ...

    @property
    def secondary_vertical_axis(self) -> IAxis:
        """Gets the chart's secondary vertical axis. Read-only ."""
        ...

    @property
    def series_axis(self) -> IAxis:
        """Gets the chart's series axis. Read-only ."""
        ...

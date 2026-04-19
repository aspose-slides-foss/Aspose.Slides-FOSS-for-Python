from __future__ import annotations
from typing import TYPE_CHECKING
from .IChartSeriesGroupCollection import IChartSeriesGroupCollection

if TYPE_CHECKING:
    from .ChartSeriesGroup import ChartSeriesGroup


class ChartSeriesGroupCollection(IChartSeriesGroupCollection):
    """Collection of ChartSeriesGroup objects.

    Built dynamically from the chart-type elements in ``<c:plotArea>``.
    Each distinct chart-type element (e.g. ``<c:barChart>``,
    ``<c:lineChart>``) becomes one group.
    """

    def __len__(self) -> int:
        return len(self._groups)

    def __getitem__(self, index: int) -> ChartSeriesGroup:
        return self._groups[index]

    def __iter__(self):
        return iter(self._groups)

    def _init_internal(self, groups: list):
        self._groups: list[ChartSeriesGroup] = list(groups)

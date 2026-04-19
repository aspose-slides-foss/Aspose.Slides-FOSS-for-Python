from __future__ import annotations
from typing import TYPE_CHECKING

from .._internal.base_collection import BaseCollection
from .ILegendEntryCollection import ILegendEntryCollection

if TYPE_CHECKING:
    from .._internal.pptx.chart_part import ChartPart
    from .LegendEntryProperties import LegendEntryProperties


class LegendEntryCollection(ILegendEntryCollection, BaseCollection):
    """Collection of legend entries.

    The collection size equals the number of series in the chart.
    Each entry is a :class:`LegendEntryProperties` keyed by series index.
    """

    def _init_internal(self, legend_elem, chart_part: 'ChartPart', series_count: int):
        self._legend_elem = legend_elem
        self._chart_part = chart_part
        self._entries: list[LegendEntryProperties] = []
        self._build(series_count)
        return self

    def _build(self, series_count: int):
        from .LegendEntryProperties import LegendEntryProperties
        self._entries = []
        for i in range(series_count):
            ep = LegendEntryProperties()
            ep._init_internal(i, self._legend_elem, self._chart_part)
            self._entries.append(ep)

    @property
    def count(self) -> int:
        return len(self._entries)

    def __len__(self):
        return len(self._entries)

    def __getitem__(self, index):
        if index < 0 or index >= len(self._entries):
            raise IndexError(f"Legend entry index {index} out of range")
        return self._entries[index]

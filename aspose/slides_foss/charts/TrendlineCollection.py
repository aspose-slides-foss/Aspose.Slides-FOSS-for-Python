from __future__ import annotations
from typing import TYPE_CHECKING

from .Trendline import Trendline
from .TrendlineType import TrendlineType
from .ITrendlineCollection import ITrendlineCollection

if TYPE_CHECKING:
    from .._internal.pptx.chart_part import ChartPart
    from .ITrendline import ITrendline


class TrendlineCollection(ITrendlineCollection):
    """Represents a collection of Trendline objects for a chart series."""

    def __len__(self) -> int:
        return len(self._trendlines)

    def __getitem__(self, index: int) -> Trendline:
        return self._trendlines[index]

    def __iter__(self):
        return iter(self._trendlines)

    @property
    def count(self) -> int:
        return len(self._trendlines)

    def add(self, trendline_type: TrendlineType) -> ITrendline:
        """Add a new trendline of the specified type."""
        tl = Trendline()
        tl._init_internal(trendline_type, chart_part=self._chart_part)
        self._trendlines.append(tl)
        return tl

    def remove(self, value: Trendline) -> None:
        """Remove a trendline from the collection."""
        self._trendlines.remove(value)

    def _init_internal(self, chart_part: 'ChartPart' = None):
        self._trendlines: list[Trendline] = []
        self._chart_part = chart_part

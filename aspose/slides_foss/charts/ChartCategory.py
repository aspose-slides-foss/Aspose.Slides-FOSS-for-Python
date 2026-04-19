from __future__ import annotations
from typing import TYPE_CHECKING
from .IChartCategory import IChartCategory

if TYPE_CHECKING:
    from .ChartDataCell import ChartDataCell
    from .IChartDataCell import IChartDataCell


class ChartCategory(IChartCategory):
    """Represents a chart category."""

    @property
    def use_cell(self) -> bool:
        return self._cell is not None

    @property
    def as_cell(self) -> IChartDataCell:
        return self._cell

    @as_cell.setter
    def as_cell(self, value: ChartDataCell):
        self._cell = value

    @property
    def as_literal(self) -> object:
        return self._literal

    @as_literal.setter
    def as_literal(self, value: object):
        self._literal = value
        self._cell = None

    @property
    def value(self) -> object:
        if self._cell is not None:
            return self._cell.value
        return self._literal

    @value.setter
    def value(self, value: object):
        if self._cell is not None:
            self._cell.value = value
        else:
            self._literal = value

    def remove(self) -> None:
        if self._parent_collection is not None:
            self._parent_collection._remove_category(self)

    def _init_internal(self, cell: 'ChartDataCell' = None, literal=None,
                       parent_collection=None):
        self._cell = cell
        self._literal = literal
        self._parent_collection = parent_collection

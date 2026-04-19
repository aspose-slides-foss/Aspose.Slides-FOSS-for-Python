from __future__ import annotations
from typing import TYPE_CHECKING, Union

from .ChartCategory import ChartCategory
from .IChartCategoryCollection import IChartCategoryCollection

if TYPE_CHECKING:
    from .ChartDataCell import ChartDataCell
    from .IChartCategory import IChartCategory


class ChartCategoryCollection(IChartCategoryCollection):
    """Represents collection of chart categories."""

    def __len__(self) -> int:
        return len(self._categories)

    def __getitem__(self, index: int) -> ChartCategory:
        return self._categories[index]

    def __iter__(self):
        return iter(self._categories)

    @property
    def use_cells(self) -> bool:
        return self._use_cells

    @use_cells.setter
    def use_cells(self, value: bool):
        self._use_cells = value

    def add(self, value) -> IChartCategory:
        """Add a category. value can be a ChartDataCell or a literal."""
        cat = ChartCategory()
        if hasattr(value, '_init_internal') and hasattr(value, 'row'):
            # ChartDataCell
            cat._init_internal(cell=value, parent_collection=self)
        else:
            cat._init_internal(literal=value, parent_collection=self)
        self._categories.append(cat)
        return cat

    def index_of(self, value: ChartCategory) -> int:
        return self._categories.index(value)

    def remove(self, value: ChartCategory) -> None:
        self._categories.remove(value)

    def remove_at(self, index: int) -> None:
        del self._categories[index]

    def clear(self) -> None:
        self._categories.clear()

    def _remove_category(self, cat: ChartCategory) -> None:
        if cat in self._categories:
            self._categories.remove(cat)

    def _init_internal(self, use_cells: bool = True):
        self._categories: list[ChartCategory] = []
        self._use_cells = use_cells

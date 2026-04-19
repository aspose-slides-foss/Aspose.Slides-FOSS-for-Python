from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .IChartCategoryLevelsManager import IChartCategoryLevelsManager
    from .IChartDataCell import IChartDataCell

class IChartCategory(ABC):
    """Represents chart categories."""
    @property
    def use_cell(self) -> bool:
        """If true then AsCell property is actual. In other words, worksheet is used for storing category (this case supports a multi-level category). If false then AsLiteral property is actual. In other words, worksheet is NOT used for storing category (and this case doesn't support a multi-level categories). Read-only ."""
        ...

    @property
    def as_cell(self) -> IChartDataCell:
        """Returns or sets IChartDataCell object. If category is multi-level then used IChartDataCell object for level "0". Read/write ."""
        ...

    @as_cell.setter
    def as_cell(self, value: IChartDataCell):
        ...

    @property
    def as_literal(self) -> object:
        """Returns or sets AsLiteral if UseCell is false. Read/write ."""
        ...

    @as_literal.setter
    def as_literal(self, value: object):
        ...

    @property
    def value(self) -> object:
        """If UseCell is true then this property represents AsCell.Value property. If UseCell is false then this property represents AsLiteral property. Read/write ."""
        ...

    @value.setter
    def value(self, value: object):
        ...

    def remove(self) -> None:
        ...

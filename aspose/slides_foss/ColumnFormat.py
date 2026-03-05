from __future__ import annotations
from typing import TYPE_CHECKING
from .IColumnFormat import IColumnFormat
if TYPE_CHECKING:
    from .IColumnFormatEffectiveData import IColumnFormatEffectiveData

class ColumnFormat(IColumnFormat):
    pass

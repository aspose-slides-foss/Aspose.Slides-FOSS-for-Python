from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ShapeAdjustmentType import ShapeAdjustmentType

class IAdjustValue(ABC):
    """Represents a geometry shape's adjustment value. These values affect shape's form."""
    @property
    def raw_value(self) -> int:
        """Returns or sets adjustment value "as is". Read/write ."""
        ...

    @raw_value.setter
    def raw_value(self, value: int):
        ...

    @property
    def angle_value(self) -> float:
        """Returns or sets value, interpreting it as angle in degrees. Read/write ."""
        ...

    @angle_value.setter
    def angle_value(self, value: float):
        ...

    @property
    def name(self) -> str:
        """Returns a name of this adjustment value. Read-only ."""
        ...



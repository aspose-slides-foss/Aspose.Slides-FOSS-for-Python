from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .BevelPresetType import BevelPresetType

class IShapeBevel(ABC):
    """Represents properties of shape's main face relief."""
    @property
    def width(self) -> float:
        """Bevel width. Read/write ."""
        ...

    @width.setter
    def width(self, value: float):
        ...

    @property
    def height(self) -> float:
        """Bevel height. Read/write ."""
        ...

    @height.setter
    def height(self, value: float):
        ...

    @property
    def bevel_type(self) -> BevelPresetType:
        """Bevel type. Read/write ."""
        ...

    @bevel_type.setter
    def bevel_type(self, value: BevelPresetType):
        ...


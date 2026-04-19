from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .IFormat import IFormat
    from .PictureType import PictureType

class IChartWall(ABC):
    """Represents walls on 3d charts."""
    @property
    def thickness(self) -> int:
        """Returns or sets the walls thickness as a percentage of the largest dimension of the plot volume. Read/write ."""
        ...

    @thickness.setter
    def thickness(self, value: int):
        ...

    @property
    def format(self) -> IFormat:
        """Returns the wall fill, line, effect, 3d styles. Read-only ."""
        ...

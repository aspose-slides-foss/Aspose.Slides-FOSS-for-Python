from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IShape import IShape

if TYPE_CHECKING:
    from .IGroupShapeLock import IGroupShapeLock
    from .IShapeCollection import IShapeCollection

class IGroupShape(IShape, ABC):
    """Represents a group of shapes on a slide."""
    @property
    @abstractmethod
    def group_shape_lock(self) -> IGroupShapeLock:
        """Returns shape's locks. Read-only ."""
        ...

    @property
    @abstractmethod
    def shapes(self) -> IShapeCollection:
        """Returns the collection of shapes inside the group. Read-only ."""
        ...

    @property
    @abstractmethod
    def as_i_shape(self) -> IShape:
        """Allows to get base IShape interface. Read-only ."""
        ...

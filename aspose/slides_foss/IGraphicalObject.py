from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING
from .IShape import IShape

if TYPE_CHECKING:
    from .IGraphicalObjectLock import IGraphicalObjectLock

class IGraphicalObject(IShape, ABC):
    """Represents abstract graphical object."""
    @property
    def graphical_object_lock(self) -> IGraphicalObjectLock:
        """Returns shape's locks. Read-only ."""
        ...


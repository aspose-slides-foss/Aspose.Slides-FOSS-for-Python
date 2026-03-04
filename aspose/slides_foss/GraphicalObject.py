from __future__ import annotations
from typing import overload, TYPE_CHECKING
from abc import ABC, abstractmethod
from .Shape import Shape
from .IGraphicalObject import IGraphicalObject
if TYPE_CHECKING:
    from .ICustomData import ICustomData
    from .IGraphicalObjectLock import IGraphicalObjectLock
    from .IPlaceholder import IPlaceholder

class GraphicalObject(Shape, IGraphicalObject, ABC):
    pass

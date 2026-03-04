from __future__ import annotations
from typing import overload, TYPE_CHECKING
from .Shape import Shape
if TYPE_CHECKING:
    from .ICustomData import ICustomData
    from .IGroupShapeLock import IGroupShapeLock
    from .IPlaceholder import IPlaceholder
    from .IShapeCollection import IShapeCollection

class GroupShape(Shape):
    pass

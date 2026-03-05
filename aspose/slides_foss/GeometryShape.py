from __future__ import annotations
from typing import overload, TYPE_CHECKING
from abc import ABC, abstractmethod
from .Shape import Shape
from .IGeometryShape import IGeometryShape
if TYPE_CHECKING:
    from .IAdjustValueCollection import IAdjustValueCollection
    from .ShapeType import ShapeType

class GeometryShape(Shape, IGeometryShape, ABC):
    pass

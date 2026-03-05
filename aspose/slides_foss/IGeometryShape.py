from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING
from .IShape import IShape

if TYPE_CHECKING:
    from .IAdjustValueCollection import IAdjustValueCollection
    from .ShapeType import ShapeType

class IGeometryShape(IShape, ABC):
    """Represents the parent class for all geometric shapes."""
    @property
    def shape_style(self) -> IShapeStyle:
        """Returns shape's style object. Read-only ."""
        ...

    @property
    def shape_type(self) -> ShapeType:
        """Returns or sets the geometry preset type. Note: on value changing all adjustment values will reset to their default values. Read/write ."""
        ...

    @shape_type.setter
    def shape_type(self, value: ShapeType):
        ...

    @property
    def adjustments(self) -> IAdjustValueCollection:
        """Returns a collection of shape's adjustment values. Read-only ."""
        ...






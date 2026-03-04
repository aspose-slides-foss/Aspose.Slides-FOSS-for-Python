from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING
from .IGeometryShape import IGeometryShape

if TYPE_CHECKING:
    from .IAutoShapeLock import IAutoShapeLock
    from .ITextFrame import ITextFrame

class IAutoShape(IGeometryShape, ABC):
    """Represents an AutoShape."""

    @property
    def text_frame(self) -> ITextFrame:
        """Returns TextFrame object for the AutoShape. Read-only ."""
        ...



    @property
    def is_text_box(self) -> bool:
        """Specifies if the shape is a text box."""
        ...

    @property
    def as_i_geometry_shape(self) -> IGeometryShape:
        """Allows to get base IGeometryShape interface. Read-only ."""
        ...
    def add_text_frame(self, text) -> ITextFrame:
        ...

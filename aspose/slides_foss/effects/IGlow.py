from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IImageTransformOperation import IImageTransformOperation

if TYPE_CHECKING:
    from ..IColorFormat import IColorFormat

class IGlow(IImageTransformOperation, ABC):
    """Represents a Glow effect, in which a color blurred outline is added outside the edges of the object."""
    @property
    def radius(self) -> float:
        """Radius. Read/write ."""
        ...

    @radius.setter
    def radius(self, value: float):
        ...

    @property
    def color(self) -> IColorFormat:
        """Color format. Read-only ."""
        ...

    @property
    def as_i_image_transform_operation(self) -> IImageTransformOperation:
        """Allows to get base IImageTransformOperation interface. Read-only ."""
        ...



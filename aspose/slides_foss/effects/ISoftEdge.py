from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IImageTransformOperation import IImageTransformOperation

if TYPE_CHECKING:
    from .ISoftEdgeEffectiveData import ISoftEdgeEffectiveData

class ISoftEdge(IImageTransformOperation, ABC):
    """Represents a Soft Edge effect. The edges of the shape are blurred, while the fill is not affected."""
    @property
    def radius(self) -> float:
        """Specifies the radius of blur to apply to the edges. Read/write ."""
        ...

    @radius.setter
    def radius(self, value: float):
        ...

    @property
    def as_i_image_transform_operation(self) -> IImageTransformOperation:
        """Allows to get base IImageTransformOperation interface. Read-only ."""
        ...



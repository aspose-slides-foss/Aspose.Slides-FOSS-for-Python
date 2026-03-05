from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IImageTransformOperation import IImageTransformOperation

if TYPE_CHECKING:
    from ..FillBlendMode import FillBlendMode
    from ..IFillFormat import IFillFormat

class IFillOverlay(IImageTransformOperation, ABC):
    """Represents a Fill Overlay effect. A fill overlay may be used to specify an additional fill for an object and blend the two fills together."""
    @property
    def blend(self) -> FillBlendMode:
        """FillBlendMode. Read/write ."""
        ...

    @blend.setter
    def blend(self, value: FillBlendMode):
        ...

    @property
    def fill_format(self) -> IFillFormat:
        """Fill format. Read-only ."""
        ...

    @property
    def as_i_image_transform_operation(self) -> IImageTransformOperation:
        """Allows to get base IImageTransformOperation interface. Read-only ."""
        ...



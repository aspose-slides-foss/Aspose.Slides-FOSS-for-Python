from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IImageTransformOperation import IImageTransformOperation

if TYPE_CHECKING:
    from .IBlurEffectiveData import IBlurEffectiveData

class IBlur(IImageTransformOperation, ABC):
    """Represents a Blur effect that is applied to the entire shape, including its fill. All color channels, including alpha, are affected."""
    @property
    def radius(self) -> float:
        """Returns or sets blur radius. Read/write ."""
        ...

    @radius.setter
    def radius(self, value: float):
        ...

    @property
    def grow(self) -> bool:
        """Determines whether the bounds of the object should be grown as a result of the blurring. True indicates the bounds are grown while false indicates that they are not. Read/write ."""
        ...

    @grow.setter
    def grow(self, value: bool):
        ...

    @property
    def as_i_image_transform_operation(self) -> IImageTransformOperation:
        """Allows to get base IImageTransformOperation interface. Read-only ."""
        ...



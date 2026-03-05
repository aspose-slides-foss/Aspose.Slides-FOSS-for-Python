from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IFillParamSource import IFillParamSource

if TYPE_CHECKING:
    from .FillType import FillType
    from .IColorFormat import IColorFormat
    from .IGradientFormat import IGradientFormat
    from .IPatternFormat import IPatternFormat
    from .NullableBool import NullableBool

class ILineFillFormat(IFillParamSource, ABC):
    """Represents properties for lines filling."""
    @property
    def fill_type(self) -> FillType:
        """Returns or sets the fill type. Read/write ."""
        ...

    @fill_type.setter
    def fill_type(self, value: FillType):
        ...

    @property
    def solid_fill_color(self) -> IColorFormat:
        """Returns the color of a solid fill. Read-only ."""
        ...

    @property
    def gradient_format(self) -> IGradientFormat:
        """Returns the gradient fill format. Read-only ."""
        ...

    @property
    def pattern_format(self) -> IPatternFormat:
        """Returns the pattern fill format. Read-only ."""
        ...

    @property
    def rotate_with_shape(self) -> NullableBool:
        """Determines whether the fill should be rotated with a shape. Read/write ."""
        ...

    @rotate_with_shape.setter
    def rotate_with_shape(self, value: NullableBool):
        ...



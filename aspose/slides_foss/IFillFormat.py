from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IFillParamSource import IFillParamSource

if TYPE_CHECKING:
    from .FillType import FillType
    from .IColorFormat import IColorFormat
    from .IFillFormatEffectiveData import IFillFormatEffectiveData
    from .IGradientFormat import IGradientFormat
    from .IPatternFormat import IPatternFormat
    from .IPictureFillFormat import IPictureFillFormat
    from .NullableBool import NullableBool

class IFillFormat(IFillParamSource, ABC):
    """Represents a fill formatting options."""
    @property
    def fill_type(self) -> FillType:
        """Returns or sets the type of filling. Read/write ."""
        ...

    @fill_type.setter
    def fill_type(self, value: FillType):
        ...

    @property
    def solid_fill_color(self) -> IColorFormat:
        """Returns the fill color. Read-only ."""
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
    def picture_fill_format(self) -> IPictureFillFormat:
        """Returns the picture fill format. Read-only ."""
        ...

    @property
    def rotate_with_shape(self) -> NullableBool:
        """Determines whether the fill should be rotated with shape. Read/write ."""
        ...

    @rotate_with_shape.setter
    def rotate_with_shape(self, value: NullableBool):
        ...




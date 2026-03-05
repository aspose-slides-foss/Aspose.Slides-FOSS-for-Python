from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IFillParamSource import IFillParamSource

if TYPE_CHECKING:
    from .GradientDirection import GradientDirection
    from .GradientShape import GradientShape
    from .IGradientStopCollection import IGradientStopCollection
    from .NullableBool import NullableBool
    from .TileFlip import TileFlip

class IGradientFormat(IFillParamSource, ABC):
    """Represent a gradient format."""
    @property
    def tile_flip(self) -> TileFlip:
        """Returns or sets the flipping mode for a gradient. Read/write ."""
        ...

    @tile_flip.setter
    def tile_flip(self, value: TileFlip):
        ...

    @property
    def gradient_direction(self) -> GradientDirection:
        """Returns or sets the style of a gradient. Read/write ."""
        ...

    @gradient_direction.setter
    def gradient_direction(self, value: GradientDirection):
        ...

    @property
    def linear_gradient_angle(self) -> float:
        """Returns or sets the angle of a gradient. Read/write ."""
        ...

    @linear_gradient_angle.setter
    def linear_gradient_angle(self, value: float):
        ...

    @property
    def linear_gradient_scaled(self) -> NullableBool:
        """Determines whether a gradient is scaled. Read/write ."""
        ...

    @linear_gradient_scaled.setter
    def linear_gradient_scaled(self, value: NullableBool):
        ...

    @property
    def gradient_shape(self) -> GradientShape:
        """Returns or sets the shape of a gradient. Read/write ."""
        ...

    @gradient_shape.setter
    def gradient_shape(self, value: GradientShape):
        ...

    @property
    def gradient_stops(self) -> IGradientStopCollection:
        """Returns the collection of gradient stops. Read-only ."""
        ...



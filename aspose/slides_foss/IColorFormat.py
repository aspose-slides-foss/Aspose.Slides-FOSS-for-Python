from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IFillParamSource import IFillParamSource

if TYPE_CHECKING:
    from .drawing import Color
    from .ColorType import ColorType
    from .PresetColor import PresetColor
    from .SchemeColor import SchemeColor

class IColorFormat(IFillParamSource, ABC):
    """Represents a color used in a presentation."""
    @property
    def color_type(self) -> ColorType:
        """Returns or sets the color definition method. Read/write ."""
        ...

    @color_type.setter
    def color_type(self, value: ColorType):
        ...

    @property
    def color(self) -> Color:
        """Returns resulting color (with all color transformations applied). Sets RGB colors and clears all color transformations. Read/write ."""
        ...

    @color.setter
    def color(self, value: Color):
        ...

    @property
    def preset_color(self) -> PresetColor:
        """Returns or sets the color preset. Read/write ."""
        ...

    @preset_color.setter
    def preset_color(self, value: PresetColor):
        ...



    @property
    def scheme_color(self) -> SchemeColor:
        """Returns or sets the color identified by a color scheme. Read/write ."""
        ...

    @scheme_color.setter
    def scheme_color(self, value: SchemeColor):
        ...

    @property
    def r(self) -> int:
        """Returns or sets the red component of a color. All color transformations are ignored. Read/write ."""
        ...

    @r.setter
    def r(self, value: int):
        ...

    @property
    def g(self) -> int:
        """Returns or sets the green component of a color. All color transformations are ignored. Read/write ."""
        ...

    @g.setter
    def g(self, value: int):
        ...

    @property
    def b(self) -> int:
        """Returns or sets the blue component of a color. All color transformations are ignored. Read/write ."""
        ...

    @b.setter
    def b(self, value: int):
        ...

    @property
    def float_r(self) -> float:
        """Returns or sets the red component of a color. All color transformations are ignored. Read/write ."""
        ...

    @float_r.setter
    def float_r(self, value: float):
        ...

    @property
    def float_g(self) -> float:
        """Returns or sets the green component of a color. All color transformations are ignored. Read/write ."""
        ...

    @float_g.setter
    def float_g(self, value: float):
        ...

    @property
    def float_b(self) -> float:
        """Returns or sets the blue component of a color. All color transformations are ignored. Read/write ."""
        ...

    @float_b.setter
    def float_b(self, value: float):
        ...












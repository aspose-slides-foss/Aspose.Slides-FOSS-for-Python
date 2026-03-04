from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IImageTransformOperation import IImageTransformOperation

if TYPE_CHECKING:
    from ..IColorFormat import IColorFormat
    from .IOuterShadowEffectiveData import IOuterShadowEffectiveData
    from ..RectangleAlignment import RectangleAlignment

class IOuterShadow(IImageTransformOperation, ABC):
    """Represents an Outer Shadow effect."""
    @property
    def blur_radius(self) -> float:
        """Blur radius, in points. Default value – 0 pt. Read/write ."""
        ...

    @blur_radius.setter
    def blur_radius(self, value: float):
        ...

    @property
    def direction(self) -> float:
        """Direction of the shadow, in degrees. Default value – 0 ° (left-to-right). Read/write ."""
        ...

    @direction.setter
    def direction(self, value: float):
        ...

    @property
    def distance(self) -> float:
        """Distance of the shadow from the object, in points. Default value – 0 pt. Read/write ."""
        ...

    @distance.setter
    def distance(self, value: float):
        ...

    @property
    def shadow_color(self) -> IColorFormat:
        """Color of the shadow. Default value – automatic black (theme-dependent). Read-only ."""
        ...

    @property
    def rectangle_align(self) -> RectangleAlignment:
        """Rectangle alignment. Default value – . Read/write ."""
        ...

    @rectangle_align.setter
    def rectangle_align(self, value: RectangleAlignment):
        ...

    @property
    def skew_horizontal(self) -> float:
        """Horizontal skew angle, in degrees. Default value – 0 °. Read/write ."""
        ...

    @skew_horizontal.setter
    def skew_horizontal(self, value: float):
        ...

    @property
    def skew_vertical(self) -> float:
        """Vertical skew angle, in degrees. Default value – 0 °. Read/write ."""
        ...

    @skew_vertical.setter
    def skew_vertical(self, value: float):
        ...

    @property
    def rotate_shadow_with_shape(self) -> bool:
        """Indicates whether the shadow rotates together with the shape. Default value – true. Read/write ."""
        ...

    @rotate_shadow_with_shape.setter
    def rotate_shadow_with_shape(self, value: bool):
        ...

    @property
    def scale_horizontal(self) -> float:
        """Horizontal scaling factor, in percent of the original size. Negative scaling causes a flip. Default value – 100 %. Read/write ."""
        ...

    @scale_horizontal.setter
    def scale_horizontal(self, value: float):
        ...

    @property
    def scale_vertical(self) -> float:
        """Vertical scaling factor, in percent of the original size. Negative scaling causes a flip. Default value – 100 %. Read/write ."""
        ...

    @scale_vertical.setter
    def scale_vertical(self, value: float):
        ...

    @property
    def as_i_image_transform_operation(self) -> IImageTransformOperation:
        """Allows to get base IImageTransformOperation interface. Read-only ."""
        ...



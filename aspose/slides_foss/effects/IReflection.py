from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IImageTransformOperation import IImageTransformOperation

if TYPE_CHECKING:
    from ..RectangleAlignment import RectangleAlignment

class IReflection(IImageTransformOperation, ABC):
    """Represents a reflection effect."""
    @property
    def start_pos_alpha(self) -> float:
        """Specifies the start position (along the alpha gradient ramp) of the start alpha value (percents). Read/write ."""
        ...

    @start_pos_alpha.setter
    def start_pos_alpha(self, value: float):
        ...

    @property
    def end_pos_alpha(self) -> float:
        """Specifies the end position (along the alpha gradient ramp) of the end alpha value (percents). Read/write ."""
        ...

    @end_pos_alpha.setter
    def end_pos_alpha(self, value: float):
        ...

    @property
    def fade_direction(self) -> float:
        """Specifies the direction to offset the reflection. (angle). Read/write ."""
        ...

    @fade_direction.setter
    def fade_direction(self, value: float):
        ...

    @property
    def start_reflection_opacity(self) -> float:
        """Starting reflection opacity. (percents). Read/write ."""
        ...

    @start_reflection_opacity.setter
    def start_reflection_opacity(self, value: float):
        ...

    @property
    def end_reflection_opacity(self) -> float:
        """End reflection opacity. (percents). Read/write ."""
        ...

    @end_reflection_opacity.setter
    def end_reflection_opacity(self, value: float):
        ...

    @property
    def blur_radius(self) -> float:
        """Blur radius. Read/write ."""
        ...

    @blur_radius.setter
    def blur_radius(self, value: float):
        ...

    @property
    def direction(self) -> float:
        """Direction of reflection. Read/write ."""
        ...

    @direction.setter
    def direction(self, value: float):
        ...

    @property
    def distance(self) -> float:
        """Distance of reflection. Read/write ."""
        ...

    @distance.setter
    def distance(self, value: float):
        ...

    @property
    def rectangle_align(self) -> RectangleAlignment:
        """Rectangle alignment. Read/write ."""
        ...

    @rectangle_align.setter
    def rectangle_align(self, value: RectangleAlignment):
        ...

    @property
    def skew_horizontal(self) -> float:
        """Specifies the horizontal skew angle. Read/write ."""
        ...

    @skew_horizontal.setter
    def skew_horizontal(self, value: float):
        ...

    @property
    def skew_vertical(self) -> float:
        """Specifies the vertical skew angle. Read/write ."""
        ...

    @skew_vertical.setter
    def skew_vertical(self, value: float):
        ...

    @property
    def rotate_shadow_with_shape(self) -> bool:
        """Specifies whether the reflection should rotate with the shape if the shape is rotated. Read/write ."""
        ...

    @rotate_shadow_with_shape.setter
    def rotate_shadow_with_shape(self, value: bool):
        ...

    @property
    def scale_horizontal(self) -> float:
        """Specifies the horizontal scaling factor, negative scaling causes a flip. (percents) Read/write ."""
        ...

    @scale_horizontal.setter
    def scale_horizontal(self, value: float):
        ...

    @property
    def scale_vertical(self) -> float:
        """Specifies the vertical scaling factor, negative scaling causes a flip. (percents) Read/write ."""
        ...

    @scale_vertical.setter
    def scale_vertical(self, value: float):
        ...

    @property
    def as_i_image_transform_operation(self) -> IImageTransformOperation:
        """Allows to get base IImageTransformOperation interface. Read-only ."""
        ...



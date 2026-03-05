from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IImageTransformOperation import IImageTransformOperation

if TYPE_CHECKING:
    from ..IColorFormat import IColorFormat
    from ..PresetShadowType import PresetShadowType

class IPresetShadow(IImageTransformOperation, ABC):
    """Represents a Preset Shadow effect."""
    @property
    def direction(self) -> float:
        """Direction of shadow. Read/write ."""
        ...

    @direction.setter
    def direction(self, value: float):
        ...

    @property
    def distance(self) -> float:
        """Distance of shadow. Read/write ."""
        ...

    @distance.setter
    def distance(self, value: float):
        ...

    @property
    def shadow_color(self) -> IColorFormat:
        """Color of shadow. Read-only ."""
        ...

    @property
    def preset(self) -> PresetShadowType:
        """Preset. Read/write ."""
        ...

    @preset.setter
    def preset(self, value: PresetShadowType):
        ...

    @property
    def as_i_image_transform_operation(self) -> IImageTransformOperation:
        """Allows to get base IImageTransformOperation interface. Read-only ."""
        ...



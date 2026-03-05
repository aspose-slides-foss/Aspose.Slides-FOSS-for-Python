from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .LightingDirection import LightingDirection
    from .LightRigPresetType import LightRigPresetType

class ILightRig(ABC):
    """Represents LightRig."""
    @property
    def direction(self) -> LightingDirection:
        """Light direction. Read/write ."""
        ...

    @direction.setter
    def direction(self, value: LightingDirection):
        ...

    @property
    def light_type(self) -> LightRigPresetType:
        """Represents a preset light right that can be applied to a shape. The light rig represents a group of lights oriented in a specific way relative to a 3D scene. Read/write ."""
        ...

    @light_type.setter
    def light_type(self, value: LightRigPresetType):
        ...
    def set_rotation(self, latitude, longitude, revolution) -> None:
        ...
    def get_rotation(self) -> list[float]:
        ...


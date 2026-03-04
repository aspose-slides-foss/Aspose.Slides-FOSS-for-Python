from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .CameraPresetType import CameraPresetType

class ICamera(ABC):
    """Represents Camera."""
    @property
    def camera_type(self) -> CameraPresetType:
        """Camera type Read/write ."""
        ...

    @camera_type.setter
    def camera_type(self, value: CameraPresetType):
        ...

    @property
    def field_of_view_angle(self) -> float:
        """Camera FOV (0-180 deg, field of View) Read/write ."""
        ...

    @field_of_view_angle.setter
    def field_of_view_angle(self, value: float):
        ...

    @property
    def zoom(self) -> float:
        """Camera zoom (positive value in percentage) Read/write ."""
        ...

    @zoom.setter
    def zoom(self, value: float):
        ...
    def set_rotation(self, latitude, longitude, revolution) -> None:
        ...
    def get_rotation(self) -> list[float]:
        ...


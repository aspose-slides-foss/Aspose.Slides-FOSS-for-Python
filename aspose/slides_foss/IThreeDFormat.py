from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IThreeDParamSource import IThreeDParamSource

if TYPE_CHECKING:
    from .ICamera import ICamera
    from .IColorFormat import IColorFormat
    from .ILightRig import ILightRig
    from .IShapeBevel import IShapeBevel
    from .MaterialPresetType import MaterialPresetType

class IThreeDFormat(IThreeDParamSource, ABC):
    """Represents 3-D properties."""
    @property
    def contour_width(self) -> float:
        """Returns or sets the width of a 3D contour. Read/write ."""
        ...

    @contour_width.setter
    def contour_width(self, value: float):
        ...

    @property
    def extrusion_height(self) -> float:
        """Returns or sets the height of an extrusion effect. Read/write ."""
        ...

    @extrusion_height.setter
    def extrusion_height(self, value: float):
        ...

    @property
    def depth(self) -> float:
        """Returns or sets the depth of a 3D shape. Read/write ."""
        ...

    @depth.setter
    def depth(self, value: float):
        ...

    @property
    def bevel_top(self) -> IShapeBevel:
        """Returns or sets the type of a top 3D bevel. Read-only ."""
        ...

    @property
    def bevel_bottom(self) -> IShapeBevel:
        """Returns or sets the type of a bottom 3D bevel. Read-only ."""
        ...

    @property
    def contour_color(self) -> IColorFormat:
        """Returns or sets the color of a contour. Read-only ."""
        ...

    @property
    def extrusion_color(self) -> IColorFormat:
        """Returns or sets the color of an extrusion. Read-only ."""
        ...

    @property
    def camera(self) -> ICamera:
        """Returns or sets the settings of a camera. Read-only ."""
        ...

    @property
    def light_rig(self) -> ILightRig:
        """Returns or sets the type of a light. Read-only ."""
        ...

    @property
    def material(self) -> MaterialPresetType:
        """Returns or sets the type of a material. Read/write ."""
        ...

    @material.setter
    def material(self, value: MaterialPresetType):
        ...




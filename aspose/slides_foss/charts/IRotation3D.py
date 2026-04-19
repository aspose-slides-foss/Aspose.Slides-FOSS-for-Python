from __future__ import annotations
from abc import ABC, abstractmethod

class IRotation3D(ABC):
    """Represents 3D rotation of a chart."""
    @property
    def rotation_x(self) -> int:
        """Returns or sets the rotation degree around the X-axis, i.e. in the Y direction for 3D charts (between -90 and 90 degrees). The property matches with the 21.2.2.157 rotX (X Rotation) item in ECMA-376 and with the "Y Rotation" option in PowerPoint 2007+. Read/write ."""
        ...

    @rotation_x.setter
    def rotation_x(self, value: int):
        ...

    @property
    def rotation_y(self) -> int:
        """Returns or sets the rotation degree around the Y-axis, i.e. in the X direction for 3D charts (between 0 and 360 degrees). The property matches with the 21.2.2.158 rotY (Y Rotation) item in ECMA-376 and with the "X Rotation" option in PowerPoint 2007+. Read/write ."""
        ...

    @rotation_y.setter
    def rotation_y(self, value: int):
        ...

    @property
    def perspective(self) -> int:
        """Returns or sets the perspective value (field of view angle) for 3D charts (between 0 and 100). Ignored if RightAngleAxes property value is true. Read/write ."""
        ...

    @perspective.setter
    def perspective(self, value: int):
        ...

    @property
    def right_angle_axes(self) -> bool:
        """Determines whether the chart axes are at right angles, rather than drawn in perspective. In other words it determines whether the chart angles of axes are independent from chart rotation or elevation. Read/write ."""
        ...

    @right_angle_axes.setter
    def right_angle_axes(self, value: bool):
        ...

    @property
    def depth_percents(self) -> int:
        """Returns or sets the depth of a 3D chart as a percentage of a chart width (between 20 and 2000 percent). Read/write ."""
        ...

    @depth_percents.setter
    def depth_percents(self, value: int):
        ...

    @property
    def height_percents(self) -> int:
        """Specifies the height of a 3-D chart as a percentage of the chart width (between 5 and 500 percent). Read/write ."""
        ...

    @height_percents.setter
    def height_percents(self, value: int):
        ...

from __future__ import annotations
from typing import TYPE_CHECKING, Any
from .IShapeFrame import IShapeFrame

if TYPE_CHECKING:
    from .NullableBool import NullableBool

class ShapeFrame(IShapeFrame):
    """Represents shape frame's properties."""
    def __init__(self, x, y, width, height, flip_h, flip_v, rotation_angle):
        from .NullableBool import NullableBool
        self._x = float(x)
        self._y = float(y)
        self._width = float(width)
        self._height = float(height)
        self._flip_h = flip_h if isinstance(flip_h, NullableBool) else NullableBool(flip_h)
        self._flip_v = flip_v if isinstance(flip_v, NullableBool) else NullableBool(flip_v)
        self._rotation = float(rotation_angle)

    @property
    def x(self) -> float:
        """Returns the X coordinate of the upper-left corner of a frame. Read-only ."""
        return self._x

    @property
    def y(self) -> float:
        """Returns the Y coordinate of the upper-left corner of a frame. Read-only ."""
        return self._y

    @property
    def width(self) -> float:
        """Returns the width of a frame. Read-only ."""
        return self._width

    @property
    def height(self) -> float:
        """Returns the height of a frame. Read-only ."""
        return self._height

    @property
    def rotation(self) -> float:
        """Returns the number of degrees a frame is rotated around the z-axis. A positive value indicates clockwise rotation; a negative value indicates counterclockwise rotation. Read-only ."""
        return self._rotation

    @property
    def center_x(self) -> float:
        """Returns the X coordinate of a frame's center. Read-only ."""
        return self._x + self._width / 2.0

    @property
    def center_y(self) -> float:
        """Returns the Y coordinate of a frame's center. Read-only ."""
        return self._y + self._height / 2.0

    @property
    def flip_h(self) -> NullableBool:
        """Determines whether a frame is flipped horizontally. Read-only ."""
        return self._flip_h

    @property
    def flip_v(self) -> NullableBool:
        """Determines whether a frame is flipped vertically. Read-only ."""
        return self._flip_v

    @property
    def rectangle(self) -> Any:
        """Returns the coordinates of a frame. Read-only ."""
        return (self._x, self._y, self._width, self._height)

    def clone(self) -> object:
        return ShapeFrame(self._x, self._y, self._width, self._height,
                          self._flip_h, self._flip_v, self._rotation)

    def clone_t(self) -> IShapeFrame:
        return ShapeFrame(self._x, self._y, self._width, self._height,
                          self._flip_h, self._flip_v, self._rotation)

    def equals(self, value) -> bool:
        if not isinstance(value, ShapeFrame):
            return False
        return (self._x == value._x and self._y == value._y and
                self._width == value._width and self._height == value._height and
                self._flip_h == value._flip_h and self._flip_v == value._flip_v and
                self._rotation == value._rotation)


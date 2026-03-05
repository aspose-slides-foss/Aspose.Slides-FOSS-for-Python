from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .NullableBool import NullableBool

class IShapeFrame(ABC):
    """Represents shape frame's properties."""
    @property
    def x(self) -> float:
        """Returns the X coordinate of the upper-left corner of a frame. Read-only ."""
        ...

    @property
    def y(self) -> float:
        """Returns the Y coordinate of the upper-left corner of a frame. Read-only ."""
        ...

    @property
    def width(self) -> float:
        """Returns the width of a frame. Read-only ."""
        ...

    @property
    def height(self) -> float:
        """Returns the height of a frame. Read-only ."""
        ...

    @property
    def rotation(self) -> float:
        """Returns the number of degrees a frame is rotated around the z-axis. A positive value indicates clockwise rotation; a negative value indicates counterclockwise rotation. Read-only ."""
        ...

    @property
    def center_x(self) -> float:
        """Returns the X coordinate of a frame's center. Read-only ."""
        ...

    @property
    def center_y(self) -> float:
        """Returns the Y coordinate of a frame's center. Read-only ."""
        ...

    @property
    def flip_h(self) -> NullableBool:
        """Determines whether a frame is flipped horizontally. Read-only ."""
        ...

    @property
    def flip_v(self) -> NullableBool:
        """Determines whether a frame is flipped vertically. Read-only ."""
        ...

    @property
    def rectangle(self) -> Any:
        """Returns the coordinates of a frame. Read-only ."""
        ...
    def clone_t(self) -> IShapeFrame:
        ...


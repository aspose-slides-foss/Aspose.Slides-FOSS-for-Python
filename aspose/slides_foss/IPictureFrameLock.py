from __future__ import annotations
from abc import ABC, abstractmethod

class IPictureFrameLock(ABC):
    """Determines which operations are disabled on the parent PictureFrameEx."""
    @property
    def grouping_locked(self) -> bool:
        """Determines whether an adding this shape to a group is forbidden. Read/write ."""
        ...

    @grouping_locked.setter
    def grouping_locked(self, value: bool):
        ...

    @property
    def select_locked(self) -> bool:
        """Determines whether a selecting this shape is forbidden. Read/write ."""
        ...

    @select_locked.setter
    def select_locked(self, value: bool):
        ...

    @property
    def rotation_locked(self) -> bool:
        """Determines whether a changing rotation angle of this shape is forbidden. Read/write ."""
        ...

    @rotation_locked.setter
    def rotation_locked(self, value: bool):
        ...

    @property
    def aspect_ratio_locked(self) -> bool:
        """Determines whether a shape have to preserve aspect ratio on resizing. Read/write ."""
        ...

    @aspect_ratio_locked.setter
    def aspect_ratio_locked(self, value: bool):
        ...

    @property
    def position_locked(self) -> bool:
        """Determines whether a moving this shape is forbidden. Read/write ."""
        ...

    @position_locked.setter
    def position_locked(self, value: bool):
        ...

    @property
    def size_locked(self) -> bool:
        """Determines whether a resizing this shape is forbidden. Read/write ."""
        ...

    @size_locked.setter
    def size_locked(self, value: bool):
        ...

    @property
    def edit_points_locked(self) -> bool:
        """Determines whether a direct changing of contour of this shape is forbidden. Read/write ."""
        ...

    @edit_points_locked.setter
    def edit_points_locked(self, value: bool):
        ...

    @property
    def adjust_handles_locked(self) -> bool:
        """Determines whether a changing adjust values is forbidden. Read/write ."""
        ...

    @adjust_handles_locked.setter
    def adjust_handles_locked(self, value: bool):
        ...

    @property
    def arrowheads_locked(self) -> bool:
        """Determines whether a changing arrowheads is forbidden. Read/write ."""
        ...

    @arrowheads_locked.setter
    def arrowheads_locked(self, value: bool):
        ...

    @property
    def shape_type_locked(self) -> bool:
        """Determines whether a changing of a shape type is forbidden. Read/write ."""
        ...

    @shape_type_locked.setter
    def shape_type_locked(self, value: bool):
        ...

    @property
    def crop_locked(self) -> bool:
        """Determines whether an image cropping is forbidden. Read/write ."""
        ...

    @crop_locked.setter
    def crop_locked(self, value: bool):
        ...


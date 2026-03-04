from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .BaseShapeLock import BaseShapeLock
from .IPictureFrameLock import IPictureFrameLock

if TYPE_CHECKING:
    from .IBaseShapeLock import IBaseShapeLock

# Mapping: property name -> XML attribute name on a:picLocks
_LOCK_ATTR_MAP = {
    'grouping_locked': 'noGrp',
    'select_locked': 'noSelect',
    'rotation_locked': 'noRot',
    'aspect_ratio_locked': 'noChangeAspect',
    'position_locked': 'noMove',
    'size_locked': 'noResize',
    'edit_points_locked': 'noEditPoints',
    'adjust_handles_locked': 'noAdjustHandles',
    'arrowheads_locked': 'noChangeArrowheads',
    'shape_type_locked': 'noChangeShapeType',
    'crop_locked': 'noCrop',
}


class PictureFrameLock(BaseShapeLock, IPictureFrameLock):
    """Determines which operations are disabled on the parent PictureFrame."""

    def _init_internal(self, pic_locks_element: ET._Element, slide_part) -> None:
        """
        Internal initialization with the a:picLocks XML element.

        Args:
            pic_locks_element: The a:picLocks element (may be None if absent).
            slide_part: The SlidePart for saving changes.
        """
        self._pic_locks = pic_locks_element
        self._slide_part = slide_part

    def _get_lock(self, attr_name: str) -> bool:
        """Read a lock attribute from the picLocks element."""
        if not hasattr(self, '_pic_locks') or self._pic_locks is None:
            return False
        return self._pic_locks.get(attr_name, '0') == '1'

    def _set_lock(self, attr_name: str, value: bool) -> None:
        """Write a lock attribute to the picLocks element."""
        if not hasattr(self, '_pic_locks') or self._pic_locks is None:
            return
        if value:
            self._pic_locks.set(attr_name, '1')
        else:
            if attr_name in self._pic_locks.attrib:
                del self._pic_locks.attrib[attr_name]

    @property
    def grouping_locked(self) -> bool:
        """Determines whether an adding this shape to a group is forbidden. Read/write ."""
        return self._get_lock('noGrp')

    @grouping_locked.setter
    def grouping_locked(self, value: bool):
        self._set_lock('noGrp', value)

    @property
    def select_locked(self) -> bool:
        """Determines whether a selecting this shape is forbidden. Read/write ."""
        return self._get_lock('noSelect')

    @select_locked.setter
    def select_locked(self, value: bool):
        self._set_lock('noSelect', value)

    @property
    def rotation_locked(self) -> bool:
        """Determines whether a changing rotation angle of this shape is forbidden. Read/write ."""
        return self._get_lock('noRot')

    @rotation_locked.setter
    def rotation_locked(self, value: bool):
        self._set_lock('noRot', value)

    @property
    def aspect_ratio_locked(self) -> bool:
        """Determines whether a shape have to preserve aspect ratio on resizing. Read/write ."""
        return self._get_lock('noChangeAspect')

    @aspect_ratio_locked.setter
    def aspect_ratio_locked(self, value: bool):
        self._set_lock('noChangeAspect', value)

    @property
    def position_locked(self) -> bool:
        """Determines whether a moving this shape is forbidden. Read/write ."""
        return self._get_lock('noMove')

    @position_locked.setter
    def position_locked(self, value: bool):
        self._set_lock('noMove', value)

    @property
    def size_locked(self) -> bool:
        """Determines whether a resizing this shape is forbidden. Read/write ."""
        return self._get_lock('noResize')

    @size_locked.setter
    def size_locked(self, value: bool):
        self._set_lock('noResize', value)

    @property
    def edit_points_locked(self) -> bool:
        """Determines whether a direct changing of contour of this shape is forbidden. Read/write ."""
        return self._get_lock('noEditPoints')

    @edit_points_locked.setter
    def edit_points_locked(self, value: bool):
        self._set_lock('noEditPoints', value)

    @property
    def adjust_handles_locked(self) -> bool:
        """Determines whether a changing adjust values is forbidden. Read/write ."""
        return self._get_lock('noAdjustHandles')

    @adjust_handles_locked.setter
    def adjust_handles_locked(self, value: bool):
        self._set_lock('noAdjustHandles', value)

    @property
    def arrowheads_locked(self) -> bool:
        """Determines whether a changing arrowheads is forbidden. Read/write ."""
        return self._get_lock('noChangeArrowheads')

    @arrowheads_locked.setter
    def arrowheads_locked(self, value: bool):
        self._set_lock('noChangeArrowheads', value)

    @property
    def shape_type_locked(self) -> bool:
        """Determines whether a changing of a shape type is forbidden. Read/write ."""
        return self._get_lock('noChangeShapeType')

    @shape_type_locked.setter
    def shape_type_locked(self, value: bool):
        self._set_lock('noChangeShapeType', value)

    @property
    def crop_locked(self) -> bool:
        """Determines whether an image cropping is forbidden. Read/write ."""
        return self._get_lock('noCrop')

    @crop_locked.setter
    def crop_locked(self, value: bool):
        self._set_lock('noCrop', value)

    @property
    def no_locks(self) -> bool:
        """Return True if all lock attributes are absent or '0'."""
        if not hasattr(self, '_pic_locks') or self._pic_locks is None:
            return True
        for attr_name in _LOCK_ATTR_MAP.values():
            if self._pic_locks.get(attr_name, '0') == '1':
                return False
        return True


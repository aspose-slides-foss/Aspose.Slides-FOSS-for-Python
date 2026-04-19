from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import lxml.etree as ET
from .BaseShapeLock import BaseShapeLock
from .IGroupShapeLock import IGroupShapeLock
from .IBaseShapeLock import IBaseShapeLock
from ._internal.pptx.constants import NS

if TYPE_CHECKING:
    from ._internal.pptx.slide_part import SlidePart


class GroupShapeLock(BaseShapeLock, IGroupShapeLock):
    """Determines which operations are disabled on the parent GroupShape."""

    def __init__(self):
        self._cnv_grp_sp_pr: Optional[ET._Element] = None
        self._slide_part: Optional[SlidePart] = None

    def _init_internal(self, cnv_grp_sp_pr: ET._Element, slide_part: SlidePart) -> None:
        self._cnv_grp_sp_pr = cnv_grp_sp_pr
        self._slide_part = slide_part

    def _get_locks(self) -> Optional[ET._Element]:
        if self._cnv_grp_sp_pr is None:
            return None
        return self._cnv_grp_sp_pr.find(f"{NS.A}grpSpLocks")

    def _ensure_locks(self) -> ET._Element:
        locks = self._get_locks()
        if locks is not None:
            return locks
        return ET.SubElement(self._cnv_grp_sp_pr, f"{NS.A}grpSpLocks")

    def _get_lock(self, attr: str) -> bool:
        locks = self._get_locks()
        if locks is None:
            return False
        return locks.get(attr) == '1'

    def _set_lock(self, attr: str, value: bool) -> None:
        locks = self._ensure_locks()
        if value:
            locks.set(attr, '1')
        elif attr in locks.attrib:
            del locks.attrib[attr]
        if self._slide_part:
            self._slide_part.save()

    @property
    def grouping_locked(self) -> bool:
        """Determines whether adding this shape to a group is forbidden. Read/write ."""
        return self._get_lock('noGrp')

    @grouping_locked.setter
    def grouping_locked(self, value: bool):
        self._set_lock('noGrp', value)

    @property
    def ungrouping_locked(self) -> bool:
        """Determines whether splitting this groupshape is forbidden. Read/write ."""
        return self._get_lock('noUngrp')

    @ungrouping_locked.setter
    def ungrouping_locked(self, value: bool):
        self._set_lock('noUngrp', value)

    @property
    def select_locked(self) -> bool:
        """Determines whether selecting this shape is forbidden. Read/write ."""
        return self._get_lock('noSelect')

    @select_locked.setter
    def select_locked(self, value: bool):
        self._set_lock('noSelect', value)

    @property
    def rotation_locked(self) -> bool:
        """Determines whether changing rotation angle of this shape is forbidden. Read/write ."""
        return self._get_lock('noRot')

    @rotation_locked.setter
    def rotation_locked(self, value: bool):
        self._set_lock('noRot', value)

    @property
    def aspect_ratio_locked(self) -> bool:
        """Determines whether shape have to preserve aspect ratio on resizing. Read/write ."""
        return self._get_lock('noChangeAspect')

    @aspect_ratio_locked.setter
    def aspect_ratio_locked(self, value: bool):
        self._set_lock('noChangeAspect', value)

    @property
    def position_locked(self) -> bool:
        """Determines whether moving this shape is forbidden. Read/write ."""
        return self._get_lock('noMove')

    @position_locked.setter
    def position_locked(self, value: bool):
        self._set_lock('noMove', value)

    @property
    def size_locked(self) -> bool:
        """Determines whether resizing this shape is forbidden. Read/write ."""
        return self._get_lock('noResize')

    @size_locked.setter
    def size_locked(self, value: bool):
        self._set_lock('noResize', value)

    @property
    def no_locks(self) -> bool:
        """Return true if all lock-flags are disabled. Read-only ."""
        locks = self._get_locks()
        if locks is None:
            return True
        return len(locks.attrib) == 0

    @property
    def as_i_base_shape_lock(self) -> IBaseShapeLock:
        """Allows to get base IBaseShapeLock interface. Read-only ."""
        return self

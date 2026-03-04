from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .PVIObject import PVIObject
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent
from .ILightRig import ILightRig
from ._internal.pptx.constants import NS, Elements, ROTATION_UNIT

if TYPE_CHECKING:
    from .LightingDirection import LightingDirection
    from .LightRigPresetType import LightRigPresetType
    from ._internal.pptx.slide_part import SlidePart

_LIGHT_TYPE_MAP = {
    'balanced': 'BALANCED', 'brightRm': 'BRIGHT_ROOM', 'chilly': 'CHILLY',
    'contrasting': 'CONTRASTING', 'flat': 'FLAT', 'flood': 'FLOOD',
    'freezing': 'FREEZING', 'glow': 'GLOW', 'harsh': 'HARSH',
    'legacyFlat1': 'LEGACY_FLAT1', 'legacyFlat2': 'LEGACY_FLAT2',
    'legacyFlat3': 'LEGACY_FLAT3', 'legacyFlat4': 'LEGACY_FLAT4',
    'legacyHarsh1': 'LEGACY_HARSH1', 'legacyHarsh2': 'LEGACY_HARSH2',
    'legacyHarsh3': 'LEGACY_HARSH3', 'legacyHarsh4': 'LEGACY_HARSH4',
    'legacyNormal1': 'LEGACY_NORMAL1', 'legacyNormal2': 'LEGACY_NORMAL2',
    'legacyNormal3': 'LEGACY_NORMAL3', 'legacyNormal4': 'LEGACY_NORMAL4',
    'morning': 'MORNING', 'soft': 'SOFT', 'sunrise': 'SUNRISE', 'sunset': 'SUNSET',
    'threePt': 'THREE_PT', 'twoPt': 'TWO_PT',
}
_LIGHT_TYPE_MAP_REV = {v: k for k, v in _LIGHT_TYPE_MAP.items()}

_DIR_MAP = {
    'tl': 'TOP_LEFT', 't': 'TOP', 'tr': 'TOP_RIGHT', 'r': 'RIGHT',
    'br': 'BOTTOM_RIGHT', 'b': 'BOTTOM', 'bl': 'BOTTOM_LEFT', 'l': 'LEFT',
}
_DIR_MAP_REV = {v: k for k, v in _DIR_MAP.items()}


class LightRig(PVIObject, ISlideComponent, IPresentationComponent, ILightRig):
    """Represents LightRig."""

    def _init_internal(self, scene3d_element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        self._scene3d = scene3d_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    def _get_light_rig(self) -> ET._Element | None:
        if not hasattr(self, '_scene3d'):
            return None
        return self._scene3d.find(Elements.A_LIGHT_RIG)

    def _ensure_light_rig(self) -> ET._Element:
        lr = self._get_light_rig()
        if lr is not None:
            return lr
        return ET.SubElement(self._scene3d, Elements.A_LIGHT_RIG, rig='threePt', dir='t')

    def _save(self) -> None:
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    @property
    def direction(self) -> LightingDirection:
        """Light direction. Read/write."""
        if not hasattr(self, '_scene3d'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LightingDirection import LightingDirection
        lr = self._get_light_rig()
        if lr is None:
            return LightingDirection.NOT_DEFINED
        val = lr.get('dir')
        if val is None:
            return LightingDirection.NOT_DEFINED
        name = _DIR_MAP.get(val)
        return LightingDirection[name] if name else LightingDirection.NOT_DEFINED

    @direction.setter
    def direction(self, value: LightingDirection):
        if not hasattr(self, '_scene3d'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LightingDirection import LightingDirection
        lr = self._ensure_light_rig()
        if value == LightingDirection.NOT_DEFINED:
            if 'dir' in lr.attrib:
                del lr.attrib['dir']
        else:
            ooxml_val = _DIR_MAP_REV.get(value.name)
            if ooxml_val:
                lr.set('dir', ooxml_val)
        self._save()

    @property
    def light_type(self) -> LightRigPresetType:
        """Represents a preset light right that can be applied to a shape. Read/write."""
        if not hasattr(self, '_scene3d'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LightRigPresetType import LightRigPresetType
        lr = self._get_light_rig()
        if lr is None:
            return LightRigPresetType.NOT_DEFINED
        val = lr.get('rig')
        if val is None:
            return LightRigPresetType.NOT_DEFINED
        name = _LIGHT_TYPE_MAP.get(val)
        return LightRigPresetType[name] if name else LightRigPresetType.NOT_DEFINED

    @light_type.setter
    def light_type(self, value: LightRigPresetType):
        if not hasattr(self, '_scene3d'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LightRigPresetType import LightRigPresetType
        lr = self._ensure_light_rig()
        if value == LightRigPresetType.NOT_DEFINED:
            if 'rig' in lr.attrib:
                del lr.attrib['rig']
        else:
            ooxml_val = _LIGHT_TYPE_MAP_REV.get(value.name)
            if ooxml_val:
                lr.set('rig', ooxml_val)
        self._save()

    def set_rotation(self, latitude, longitude, revolution) -> None:
        if not hasattr(self, '_scene3d'):
            raise NotImplementedError("This feature is not yet available in this version.")
        lr = self._ensure_light_rig()
        rot = lr.find(Elements.A_ROT)
        if rot is None:
            rot = ET.SubElement(lr, Elements.A_ROT)
        rot.set('lat', str(int(round(latitude * ROTATION_UNIT))))
        rot.set('lon', str(int(round(longitude * ROTATION_UNIT))))
        rot.set('rev', str(int(round(revolution * ROTATION_UNIT))))
        self._save()

    def get_rotation(self) -> list[float]:
        if not hasattr(self, '_scene3d'):
            raise NotImplementedError("This feature is not yet available in this version.")
        lr = self._get_light_rig()
        if lr is None:
            return [0.0, 0.0, 0.0]
        rot = lr.find(Elements.A_ROT)
        if rot is None:
            return [0.0, 0.0, 0.0]
        lat = int(rot.get('lat', '0')) / ROTATION_UNIT
        lon = int(rot.get('lon', '0')) / ROTATION_UNIT
        rev = int(rot.get('rev', '0')) / ROTATION_UNIT
        return [lat, lon, rev]

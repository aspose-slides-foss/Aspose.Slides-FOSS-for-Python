from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .PVIObject import PVIObject
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent
from .ICamera import ICamera
from ._internal.pptx.constants import NS, Elements, ROTATION_UNIT

if TYPE_CHECKING:
    from .CameraPresetType import CameraPresetType
    from ._internal.pptx.slide_part import SlidePart

_CAMERA_PRST_MAP = {
    'isometricBottomDown': 'ISOMETRIC_BOTTOM_DOWN', 'isometricBottomUp': 'ISOMETRIC_BOTTOM_UP',
    'isometricLeftDown': 'ISOMETRIC_LEFT_DOWN', 'isometricLeftUp': 'ISOMETRIC_LEFT_UP',
    'isometricOffAxis1Left': 'ISOMETRIC_OFF_AXIS_1_LEFT', 'isometricOffAxis1Right': 'ISOMETRIC_OFF_AXIS_1_RIGHT',
    'isometricOffAxis1Top': 'ISOMETRIC_OFF_AXIS_1_TOP', 'isometricOffAxis2Left': 'ISOMETRIC_OFF_AXIS_2_LEFT',
    'isometricOffAxis2Right': 'ISOMETRIC_OFF_AXIS_2_RIGHT', 'isometricOffAxis2Top': 'ISOMETRIC_OFF_AXIS_2_TOP',
    'isometricOffAxis3Bottom': 'ISOMETRIC_OFF_AXIS_3_BOTTOM', 'isometricOffAxis3Left': 'ISOMETRIC_OFF_AXIS_3_LEFT',
    'isometricOffAxis3Right': 'ISOMETRIC_OFF_AXIS_3_RIGHT', 'isometricOffAxis4Bottom': 'ISOMETRIC_OFF_AXIS_4_BOTTOM',
    'isometricOffAxis4Left': 'ISOMETRIC_OFF_AXIS_4_LEFT', 'isometricOffAxis4Right': 'ISOMETRIC_OFF_AXIS_4_RIGHT',
    'isometricRightDown': 'ISOMETRIC_RIGHT_DOWN', 'isometricRightUp': 'ISOMETRIC_RIGHT_UP',
    'isometricTopDown': 'ISOMETRIC_TOP_DOWN', 'isometricTopUp': 'ISOMETRIC_TOP_UP',
    'legacyObliqueBottom': 'LEGACY_OBLIQUE_BOTTOM', 'legacyObliqueBottomLeft': 'LEGACY_OBLIQUE_BOTTOM_LEFT',
    'legacyObliqueBottomRight': 'LEGACY_OBLIQUE_BOTTOM_RIGHT', 'legacyObliqueFront': 'LEGACY_OBLIQUE_FRONT',
    'legacyObliqueLeft': 'LEGACY_OBLIQUE_LEFT', 'legacyObliqueRight': 'LEGACY_OBLIQUE_RIGHT',
    'legacyObliqueTop': 'LEGACY_OBLIQUE_TOP', 'legacyObliqueTopLeft': 'LEGACY_OBLIQUE_TOP_LEFT',
    'legacyObliqueTopRight': 'LEGACY_OBLIQUE_TOP_RIGHT',
    'legacyPerspectiveBottom': 'LEGACY_PERSPECTIVE_BOTTOM', 'legacyPerspectiveBottomLeft': 'LEGACY_PERSPECTIVE_BOTTOM_LEFT',
    'legacyPerspectiveBottomRight': 'LEGACY_PERSPECTIVE_BOTTOM_RIGHT', 'legacyPerspectiveFront': 'LEGACY_PERSPECTIVE_FRONT',
    'legacyPerspectiveLeft': 'LEGACY_PERSPECTIVE_LEFT', 'legacyPerspectiveRight': 'LEGACY_PERSPECTIVE_RIGHT',
    'legacyPerspectiveTop': 'LEGACY_PERSPECTIVE_TOP', 'legacyPerspectiveTopLeft': 'LEGACY_PERSPECTIVE_TOP_LEFT',
    'legacyPerspectiveTopRight': 'LEGACY_PERSPECTIVE_TOP_RIGHT',
    'obliqueBottom': 'OBLIQUE_BOTTOM', 'obliqueBottomLeft': 'OBLIQUE_BOTTOM_LEFT',
    'obliqueBottomRight': 'OBLIQUE_BOTTOM_RIGHT', 'obliqueLeft': 'OBLIQUE_LEFT',
    'obliqueRight': 'OBLIQUE_RIGHT', 'obliqueTop': 'OBLIQUE_TOP',
    'obliqueTopLeft': 'OBLIQUE_TOP_LEFT', 'obliqueTopRight': 'OBLIQUE_TOP_RIGHT',
    'orthographicFront': 'ORTHOGRAPHIC_FRONT',
    'perspectiveAbove': 'PERSPECTIVE_ABOVE', 'perspectiveAboveLeftFacing': 'PERSPECTIVE_ABOVE_LEFT_FACING',
    'perspectiveAboveRightFacing': 'PERSPECTIVE_ABOVE_RIGHT_FACING', 'perspectiveBelow': 'PERSPECTIVE_BELOW',
    'perspectiveContrastingLeftFacing': 'PERSPECTIVE_CONTRASTING_LEFT_FACING',
    'perspectiveContrastingRightFacing': 'PERSPECTIVE_CONTRASTING_RIGHT_FACING',
    'perspectiveFront': 'PERSPECTIVE_FRONT',
    'perspectiveHeroicExtremeLeftFacing': 'PERSPECTIVE_HEROIC_EXTREME_LEFT_FACING',
    'perspectiveHeroicExtremeRightFacing': 'PERSPECTIVE_HEROIC_EXTREME_RIGHT_FACING',
    'perspectiveHeroicLeftFacing': 'PERSPECTIVE_HEROIC_LEFT_FACING',
    'perspectiveHeroicRightFacing': 'PERSPECTIVE_HEROIC_RIGHT_FACING',
    'perspectiveLeft': 'PERSPECTIVE_LEFT', 'perspectiveRelaxed': 'PERSPECTIVE_RELAXED',
    'perspectiveRelaxedModerately': 'PERSPECTIVE_RELAXED_MODERATELY', 'perspectiveRight': 'PERSPECTIVE_RIGHT',
}
_CAMERA_PRST_MAP_REV = {v: k for k, v in _CAMERA_PRST_MAP.items()}


class Camera(PVIObject, ISlideComponent, IPresentationComponent, ICamera):
    """Represents Camera."""

    def _init_internal(self, scene3d_element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        self._scene3d = scene3d_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    def _get_camera(self) -> ET._Element | None:
        if not hasattr(self, '_scene3d'):
            return None
        return self._scene3d.find(Elements.A_CAMERA)

    def _ensure_camera(self) -> ET._Element:
        cam = self._get_camera()
        if cam is not None:
            return cam
        return ET.SubElement(self._scene3d, Elements.A_CAMERA, prst='orthographicFront')

    def _save(self) -> None:
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    @property
    def camera_type(self) -> CameraPresetType:
        """Camera type. Read/write."""
        if not hasattr(self, '_scene3d'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .CameraPresetType import CameraPresetType
        cam = self._get_camera()
        if cam is None:
            return CameraPresetType.NOT_DEFINED
        val = cam.get('prst')
        if val is None:
            return CameraPresetType.NOT_DEFINED
        name = _CAMERA_PRST_MAP.get(val)
        return CameraPresetType[name] if name else CameraPresetType.NOT_DEFINED

    @camera_type.setter
    def camera_type(self, value: CameraPresetType):
        if not hasattr(self, '_scene3d'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .CameraPresetType import CameraPresetType
        cam = self._ensure_camera()
        if value == CameraPresetType.NOT_DEFINED:
            if 'prst' in cam.attrib:
                del cam.attrib['prst']
        else:
            ooxml_val = _CAMERA_PRST_MAP_REV.get(value.name)
            if ooxml_val:
                cam.set('prst', ooxml_val)
        self._save()

    @property
    def field_of_view_angle(self) -> float:
        """Camera FOV (0-180 deg, field of View). Read/write."""
        if not hasattr(self, '_scene3d'):
            raise NotImplementedError("This feature is not yet available in this version.")
        cam = self._get_camera()
        if cam is None:
            return 0.0
        fov = cam.get('fov')
        if fov is None:
            return 0.0
        return int(fov) / ROTATION_UNIT

    @field_of_view_angle.setter
    def field_of_view_angle(self, value: float):
        if not hasattr(self, '_scene3d'):
            raise NotImplementedError("This feature is not yet available in this version.")
        cam = self._ensure_camera()
        cam.set('fov', str(int(round(value * ROTATION_UNIT))))
        self._save()

    @property
    def zoom(self) -> float:
        """Camera zoom (positive value in percentage). Read/write."""
        if not hasattr(self, '_scene3d'):
            raise NotImplementedError("This feature is not yet available in this version.")
        cam = self._get_camera()
        if cam is None:
            return 100.0
        val = cam.get('zoom')
        if val is None:
            return 100.0
        return int(val) / 1000.0

    @zoom.setter
    def zoom(self, value: float):
        if not hasattr(self, '_scene3d'):
            raise NotImplementedError("This feature is not yet available in this version.")
        cam = self._ensure_camera()
        cam.set('zoom', str(int(round(value * 1000))))
        self._save()

    def set_rotation(self, latitude, longitude, revolution) -> None:
        if not hasattr(self, '_scene3d'):
            raise NotImplementedError("This feature is not yet available in this version.")
        cam = self._ensure_camera()
        rot = cam.find(Elements.A_ROT)
        if rot is None:
            rot = ET.SubElement(cam, Elements.A_ROT)
        rot.set('lat', str(int(round(latitude * ROTATION_UNIT))))
        rot.set('lon', str(int(round(longitude * ROTATION_UNIT))))
        rot.set('rev', str(int(round(revolution * ROTATION_UNIT))))
        self._save()

    def get_rotation(self) -> list[float]:
        if not hasattr(self, '_scene3d'):
            raise NotImplementedError("This feature is not yet available in this version.")
        cam = self._get_camera()
        if cam is None:
            return [0.0, 0.0, 0.0]
        rot = cam.find(Elements.A_ROT)
        if rot is None:
            return [0.0, 0.0, 0.0]
        lat = int(rot.get('lat', '0')) / ROTATION_UNIT
        lon = int(rot.get('lon', '0')) / ROTATION_UNIT
        rev = int(rot.get('rev', '0')) / ROTATION_UNIT
        return [lat, lon, rev]

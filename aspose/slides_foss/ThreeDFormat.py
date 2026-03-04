from __future__ import annotations
from typing import TYPE_CHECKING
import lxml.etree as ET
from .PVIObject import PVIObject
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent
from .IThreeDFormat import IThreeDFormat
from .IThreeDParamSource import IThreeDParamSource
from ._internal.pptx.constants import NS, Elements, EMU_PER_POINT

if TYPE_CHECKING:
    from .ICamera import ICamera
    from .IColorFormat import IColorFormat
    from .ILightRig import ILightRig
    from .IShapeBevel import IShapeBevel
    from .IThreeDFormatEffectiveData import IThreeDFormatEffectiveData
    from .MaterialPresetType import MaterialPresetType
    from ._internal.pptx.slide_part import SlidePart

_MATERIAL_MAP = {
    'clear': 'CLEAR', 'dkEdge': 'DK_EDGE', 'flat': 'FLAT',
    'legacyMatte': 'LEGACY_MATTE', 'legacyMetal': 'LEGACY_METAL',
    'legacyPlastic': 'LEGACY_PLASTIC', 'legacyWireframe': 'LEGACY_WIREFRAME',
    'matte': 'MATTE', 'metal': 'METAL', 'plastic': 'PLASTIC',
    'powder': 'POWDER', 'softEdge': 'SOFT_EDGE', 'softmetal': 'SOFTMETAL',
    'translucentPowder': 'TRANSLUCENT_POWDER', 'warmMatte': 'WARM_MATTE',
}
_MATERIAL_MAP_REV = {v: k for k, v in _MATERIAL_MAP.items()}

# Element order inside <p:spPr>: ... effectLst → scene3d → sp3d → extLst
_POST_SP3D_TAGS = {Elements.A_EXT_LST}
_POST_SCENE3D_TAGS = {Elements.A_SP_3D, Elements.A_EXT_LST}


class ThreeDFormat(PVIObject, ISlideComponent, IPresentationComponent, IThreeDFormat, IThreeDParamSource):
    """Represents 3-D properties."""

    def _init_internal(self, parent_element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        """
        Internal initialization.

        Args:
            parent_element: The XML element containing scene3d/sp3d (e.g., <p:spPr>).
            slide_part: The SlidePart for saving changes.
            parent_slide: The parent slide object.
        """
        self._parent_element = parent_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide

    def _get_sp3d(self) -> ET._Element | None:
        if not hasattr(self, '_parent_element'):
            return None
        return self._parent_element.find(Elements.A_SP_3D)

    def _ensure_sp3d(self) -> ET._Element:
        sp3d = self._get_sp3d()
        if sp3d is not None:
            return sp3d
        el = ET.Element(Elements.A_SP_3D)
        insert_before = None
        for child in self._parent_element:
            if child.tag in _POST_SP3D_TAGS:
                insert_before = child
                break
        if insert_before is not None:
            idx = list(self._parent_element).index(insert_before)
            self._parent_element.insert(idx, el)
        else:
            self._parent_element.append(el)
        return el

    def _get_scene3d(self) -> ET._Element | None:
        if not hasattr(self, '_parent_element'):
            return None
        return self._parent_element.find(Elements.A_SCENE_3D)

    def _ensure_scene3d(self) -> ET._Element:
        scene = self._get_scene3d()
        if scene is not None:
            return scene
        el = ET.Element(Elements.A_SCENE_3D)
        insert_before = None
        for child in self._parent_element:
            if child.tag in _POST_SCENE3D_TAGS:
                insert_before = child
                break
        if insert_before is not None:
            idx = list(self._parent_element).index(insert_before)
            self._parent_element.insert(idx, el)
        else:
            self._parent_element.append(el)
        return el

    def _save(self) -> None:
        if hasattr(self, '_slide_part') and self._slide_part:
            self._slide_part.save()

    @property
    def contour_width(self) -> float:
        """Returns or sets the width of a 3D contour. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        sp3d = self._get_sp3d()
        if sp3d is None:
            return 0.0
        val = sp3d.get('contourW')
        if val is None:
            return 0.0
        return int(val) / EMU_PER_POINT

    @contour_width.setter
    def contour_width(self, value: float):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        sp3d = self._ensure_sp3d()
        sp3d.set('contourW', str(int(round(value * EMU_PER_POINT))))
        self._save()

    @property
    def extrusion_height(self) -> float:
        """Returns or sets the height of an extrusion effect. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        sp3d = self._get_sp3d()
        if sp3d is None:
            return 0.0
        val = sp3d.get('extrusionH')
        if val is None:
            return 0.0
        return int(val) / EMU_PER_POINT

    @extrusion_height.setter
    def extrusion_height(self, value: float):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        sp3d = self._ensure_sp3d()
        sp3d.set('extrusionH', str(int(round(value * EMU_PER_POINT))))
        self._save()

    @property
    def depth(self) -> float:
        """Returns or sets the depth of a 3D shape. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        sp3d = self._get_sp3d()
        if sp3d is None:
            return 0.0
        val = sp3d.get('z')
        if val is None:
            return 0.0
        return int(val) / EMU_PER_POINT

    @depth.setter
    def depth(self, value: float):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        sp3d = self._ensure_sp3d()
        sp3d.set('z', str(int(round(value * EMU_PER_POINT))))
        self._save()

    @property
    def bevel_top(self) -> IShapeBevel:
        """Returns or sets the type of a top 3D bevel. Read-only."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .ShapeBevel import ShapeBevel
        sp3d = self._ensure_sp3d()
        bevel_t = sp3d.find(Elements.A_BEVEL_T)
        if bevel_t is None:
            bevel_t = ET.SubElement(sp3d, Elements.A_BEVEL_T)
        bevel = ShapeBevel(True)
        bevel._init_internal(bevel_t, self._slide_part, self._parent_slide)
        return bevel

    @property
    def bevel_bottom(self) -> IShapeBevel:
        """Returns or sets the type of a bottom 3D bevel. Read-only."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .ShapeBevel import ShapeBevel
        sp3d = self._ensure_sp3d()
        bevel_b = sp3d.find(Elements.A_BEVEL_B)
        if bevel_b is None:
            bevel_b = ET.SubElement(sp3d, Elements.A_BEVEL_B)
        bevel = ShapeBevel(False)
        bevel._init_internal(bevel_b, self._slide_part, self._parent_slide)
        return bevel

    @property
    def contour_color(self) -> IColorFormat:
        """Returns or sets the color of a contour. Read-only."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .ColorFormat import ColorFormat
        sp3d = self._ensure_sp3d()
        contour_clr = sp3d.find(Elements.A_CONTOUR_CLR)
        if contour_clr is None:
            contour_clr = ET.SubElement(sp3d, Elements.A_CONTOUR_CLR)
        cf = ColorFormat()
        cf._init_internal(contour_clr, self._slide_part, self._parent_slide)
        return cf

    @property
    def extrusion_color(self) -> IColorFormat:
        """Returns or sets the color of an extrusion. Read-only."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .ColorFormat import ColorFormat
        sp3d = self._ensure_sp3d()
        extrusion_clr = sp3d.find(Elements.A_EXTRUSION_CLR)
        if extrusion_clr is None:
            extrusion_clr = ET.SubElement(sp3d, Elements.A_EXTRUSION_CLR)
        cf = ColorFormat()
        cf._init_internal(extrusion_clr, self._slide_part, self._parent_slide)
        return cf

    @property
    def camera(self) -> ICamera:
        """Returns or sets the settings of a camera. Read-only."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .Camera import Camera
        scene3d = self._ensure_scene3d()
        cam = Camera()
        cam._init_internal(scene3d, self._slide_part, self._parent_slide)
        return cam

    @property
    def light_rig(self) -> ILightRig:
        """Returns or sets the type of a light. Read-only."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .LightRig import LightRig
        scene3d = self._ensure_scene3d()
        lr = LightRig()
        lr._init_internal(scene3d, self._slide_part, self._parent_slide)
        return lr

    @property
    def material(self) -> MaterialPresetType:
        """Returns or sets the type of a material. Read/write."""
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .MaterialPresetType import MaterialPresetType
        sp3d = self._get_sp3d()
        if sp3d is None:
            return MaterialPresetType.NOT_DEFINED
        val = sp3d.get('prstMaterial')
        if val is None:
            return MaterialPresetType.NOT_DEFINED
        name = _MATERIAL_MAP.get(val)
        return MaterialPresetType[name] if name else MaterialPresetType.NOT_DEFINED

    @material.setter
    def material(self, value: MaterialPresetType):
        if not hasattr(self, '_parent_element'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .MaterialPresetType import MaterialPresetType
        sp3d = self._ensure_sp3d()
        if value == MaterialPresetType.NOT_DEFINED:
            if 'prstMaterial' in sp3d.attrib:
                del sp3d.attrib['prstMaterial']
        else:
            ooxml_val = _MATERIAL_MAP_REV.get(value.name)
            if ooxml_val:
                sp3d.set('prstMaterial', ooxml_val)
        self._save()



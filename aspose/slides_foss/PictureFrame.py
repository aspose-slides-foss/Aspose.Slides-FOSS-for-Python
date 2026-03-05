from __future__ import annotations
from typing import overload, TYPE_CHECKING
import lxml.etree as ET
from .GeometryShape import GeometryShape
from .IPictureFrame import IPictureFrame
from ._internal.pptx.constants import NS, Attributes

if TYPE_CHECKING:
    from .IAdjustValueCollection import IAdjustValueCollection
    from .IGeometryShape import IGeometryShape
    from .IPictureFillFormat import IPictureFillFormat
    from .IPictureFrameLock import IPictureFrameLock
    from .ShapeType import ShapeType

class PictureFrame(GeometryShape, IPictureFrame):
    """Represents a frame with a picture inside."""


    @property
    def shape_type(self) -> ShapeType:
        """Returns or sets the AutoShape type for a PictureFrame. There are allowable all items of the set , except all sorts of lines: ShapeType.Line, ShapeType.StraightConnector1, ShapeType.BentConnector2, ShapeType.BentConnector3, ShapeType.BentConnector4, ShapeType.BentConnector5, ShapeType.CurvedConnector2, ShapeType.CurvedConnector3, ShapeType.CurvedConnector4, ShapeType.CurvedConnector5. Read/write ."""
        if self._xml_element is None:
            return None
        from .ShapeType import ShapeType
        from ._internal.pptx.shape_type_mapping import ooxml_prst_to_shape_type_name
        sp_pr = self._xml_element.find(f'{NS.P}spPr')
        if sp_pr is None:
            return ShapeType.RECTANGLE
        prst_geom = sp_pr.find(f'{NS.A}prstGeom')
        if prst_geom is None:
            return ShapeType.RECTANGLE
        prst = prst_geom.get('prst', 'rect')
        type_name = ooxml_prst_to_shape_type_name(prst)
        if type_name is None:
            return ShapeType.RECTANGLE
        return ShapeType[type_name]

    @shape_type.setter
    def shape_type(self, value: ShapeType):
        if self._xml_element is None:
            return
        from ._internal.pptx.shape_type_mapping import shape_type_name_to_ooxml_prst
        prst = shape_type_name_to_ooxml_prst(value.name)
        if prst is None:
            prst = 'rect'
        sp_pr = self._xml_element.find(f'{NS.P}spPr')
        if sp_pr is None:
            return
        prst_geom = sp_pr.find(f'{NS.A}prstGeom')
        if prst_geom is None:
            prst_geom = ET.SubElement(sp_pr, f'{NS.A}prstGeom')
        prst_geom.set('prst', prst)


    @property
    def picture_frame_lock(self) -> IPictureFrameLock:
        """Returns shape's locks. Read-only ."""
        if self._xml_element is None:
            return None
        from .PictureFrameLock import PictureFrameLock
        # Find a:picLocks inside p:nvPicPr/p:cNvPicPr
        nv_pic_pr = self._xml_element.find(f'{NS.P}nvPicPr')
        pic_locks = None
        if nv_pic_pr is not None:
            c_nv_pic_pr = nv_pic_pr.find(f'{NS.P}cNvPicPr')
            if c_nv_pic_pr is not None:
                pic_locks = c_nv_pic_pr.find(f'{NS.A}picLocks')
                if pic_locks is None:
                    pic_locks = ET.SubElement(c_nv_pic_pr, f'{NS.A}picLocks')
        lock = PictureFrameLock()
        lock._init_internal(pic_locks, self._slide_part)
        return lock

    @property
    def picture_format(self) -> IPictureFillFormat:
        """Returns the PictureFillFormat object for a picture frame. Read-only ."""
        if self._xml_element is None:
            return None
        from .PictureFillFormat import PictureFillFormat
        blip_fill = self._xml_element.find(f'{NS.P}blipFill')
        if blip_fill is None:
            return None
        fmt = PictureFillFormat()
        fmt._init_internal(blip_fill, self._slide_part, self._parent_slide)
        return fmt

    @property
    def relative_scale_height(self) -> float:
        """Returns or sets the scale of height(relative to original picture size) of the picture frame. Value 1.0 corresponds to 100%. Read/write ."""
        return getattr(self, '_relative_scale_height', 1.0)

    @relative_scale_height.setter
    def relative_scale_height(self, value: float):
        self._relative_scale_height = value

    @property
    def relative_scale_width(self) -> float:
        """Returns or sets the scale of width (relative to original picture size) of the picture frame. Value 1.0 corresponds to 100%. Read/write ."""
        return getattr(self, '_relative_scale_width', 1.0)

    @relative_scale_width.setter
    def relative_scale_width(self, value: float):
        self._relative_scale_width = value

    @property
    def is_cameo(self) -> bool:
        """Determines whether the PictureFrame is Cameo object or not. Read only ."""
        return False


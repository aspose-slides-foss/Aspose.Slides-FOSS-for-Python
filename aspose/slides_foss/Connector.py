from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import lxml.etree as ET
from .GeometryShape import GeometryShape
from .IConnector import IConnector
from ._internal.pptx.constants import NS, EMU_PER_POINT, Elements

if TYPE_CHECKING:
    from .IAdjustValueCollection import IAdjustValueCollection
    from .IGeometryShape import IGeometryShape
    from .IShape import IShape
    from .ShapeType import ShapeType

class Connector(GeometryShape, IConnector):
    """Represents a connector."""

    @property
    def is_text_holder(self) -> bool:
        return False

    @property
    def placeholder(self):
        return None

    @property
    def custom_data(self):
        return None

    @property
    def shape_style(self) -> IShapeStyle:
        return None

    # --- Internal helpers ---

    def _get_c_nv_cxn_sp_pr(self) -> Optional[ET._Element]:
        """Find the p:cNvCxnSpPr element."""
        if self._xml_element is None:
            return None
        nv_cxn_sp_pr = self._xml_element.find(f"{NS.P}nvCxnSpPr")
        if nv_cxn_sp_pr is None:
            return None
        return nv_cxn_sp_pr.find(f"{NS.P}cNvCxnSpPr")

    def _ensure_c_nv_cxn_sp_pr(self) -> ET._Element:
        """Get or create p:cNvCxnSpPr."""
        if self._xml_element is None:
            raise RuntimeError("Connector has no XML element")
        nv_cxn_sp_pr = self._xml_element.find(f"{NS.P}nvCxnSpPr")
        if nv_cxn_sp_pr is None:
            raise RuntimeError("Connector has no nvCxnSpPr element")
        c_nv_cxn_sp_pr = nv_cxn_sp_pr.find(f"{NS.P}cNvCxnSpPr")
        if c_nv_cxn_sp_pr is None:
            c_nv_cxn_sp_pr = ET.SubElement(nv_cxn_sp_pr, f"{NS.P}cNvCxnSpPr")
        return c_nv_cxn_sp_pr

    def _find_shape_by_id(self, shape_id: int) -> Optional[IShape]:
        """Search parent slide shapes for a shape with the given cNvPr@id."""
        if self._parent_slide is None:
            return None
        shapes = self._parent_slide.shapes
        for shape in shapes:
            c_nv_pr = shape._get_c_nv_pr() if hasattr(shape, '_get_c_nv_pr') else None
            if c_nv_pr is not None:
                id_str = c_nv_pr.get('id')
                if id_str is not None and int(id_str) == shape_id:
                    return shape
        return None

    def _get_connection_point(self, shape, site_index: int) -> tuple:
        """Returns (x, y) in points for a connection site on a shape.

        4-site model, counter-clockwise from top (matches OOXML standard for preset shapes):
          0 = top-center
          1 = left-center
          2 = bottom-center
          3 = right-center
          fallback = shape center
        """
        x = shape.x
        y = shape.y
        w = shape.width
        h = shape.height
        sites = [
            (x + w / 2, y),        # 0: top-center
            (x,         y + h / 2),# 1: left-center
            (x + w / 2, y + h),    # 2: bottom-center
            (x + w,     y + h / 2),# 3: right-center
        ]
        if 0 <= site_index < len(sites):
            return sites[site_index]
        return (x + w / 2, y + h / 2)

    # --- Public properties ---

    @property
    def shape_type(self) -> ShapeType:
        """Returns or sets the AutoShape type. Read/write ."""
        from .ShapeType import ShapeType
        from ._internal.pptx.shape_type_mapping import ooxml_prst_to_shape_type_name
        if self._xml_element is None:
            return ShapeType.NOT_DEFINED
        sp_pr = self._xml_element.find(f"{NS.P}spPr")
        if sp_pr is None:
            return ShapeType.NOT_DEFINED
        prst_geom = sp_pr.find(f"{NS.A}prstGeom")
        if prst_geom is None:
            return ShapeType.NOT_DEFINED
        prst = prst_geom.get('prst')
        if prst is None:
            return ShapeType.NOT_DEFINED
        member_name = ooxml_prst_to_shape_type_name(prst)
        if member_name is None:
            return ShapeType.NOT_DEFINED
        return ShapeType[member_name]

    @shape_type.setter
    def shape_type(self, value: ShapeType):
        from .ShapeType import ShapeType
        from ._internal.pptx.shape_type_mapping import shape_type_name_to_ooxml_prst
        if self._xml_element is None:
            return
        if value == ShapeType.NOT_DEFINED or value == ShapeType.CUSTOM:
            return
        prst = shape_type_name_to_ooxml_prst(value.name)
        if prst is None:
            return
        sp_pr = self._xml_element.find(f"{NS.P}spPr")
        if sp_pr is None:
            sp_pr = ET.SubElement(self._xml_element, f"{NS.P}spPr")
        prst_geom = sp_pr.find(f"{NS.A}prstGeom")
        if prst_geom is None:
            prst_geom = ET.SubElement(sp_pr, f"{NS.A}prstGeom")
        prst_geom.set('prst', prst)
        if self._slide_part:
            self._slide_part.save()

    @property
    def adjustments(self) -> IAdjustValueCollection:
        from .AdjustValueCollection import AdjustValueCollection
        if self._xml_element is None:
            return None
        sp_pr = self._xml_element.find(f"{NS.P}spPr")
        if sp_pr is None:
            return None
        prst_geom = sp_pr.find(f"{NS.A}prstGeom")
        if prst_geom is None:
            return None
        av_lst = prst_geom.find(f"{NS.A}avLst")
        if av_lst is None:
            av_lst = ET.SubElement(prst_geom, f"{NS.A}avLst")
        avc = AdjustValueCollection()
        avc._init_internal(av_lst, self._slide_part)
        return avc

    @property
    def connector_lock(self) -> IConnectorLock:
        """Returns connector's locks. Read-only ."""
        return None

    @property
    def start_shape_connected_to(self) -> IShape:
        """Returns or sets the shape to attach the beginning of the connector to. Read/write ."""
        c_nv_cxn_sp_pr = self._get_c_nv_cxn_sp_pr()
        if c_nv_cxn_sp_pr is None:
            return None
        st_cxn = c_nv_cxn_sp_pr.find(f"{NS.A}stCxn")
        if st_cxn is None:
            return None
        shape_id_str = st_cxn.get('id')
        if shape_id_str is None:
            return None
        return self._find_shape_by_id(int(shape_id_str))

    @start_shape_connected_to.setter
    def start_shape_connected_to(self, value: IShape):
        if value is None:
            c_nv_cxn_sp_pr = self._get_c_nv_cxn_sp_pr()
            if c_nv_cxn_sp_pr is not None:
                st_cxn = c_nv_cxn_sp_pr.find(f"{NS.A}stCxn")
                if st_cxn is not None:
                    c_nv_cxn_sp_pr.remove(st_cxn)
                if self._slide_part:
                    self._slide_part.save()
            return
        c_nv_pr = value._get_c_nv_pr() if hasattr(value, '_get_c_nv_pr') else None
        if c_nv_pr is None:
            return
        shape_id = c_nv_pr.get('id')
        if shape_id is None:
            return
        c_nv_cxn_sp_pr = self._ensure_c_nv_cxn_sp_pr()
        st_cxn = c_nv_cxn_sp_pr.find(f"{NS.A}stCxn")
        if st_cxn is None:
            st_cxn = ET.SubElement(c_nv_cxn_sp_pr, f"{NS.A}stCxn")
        st_cxn.set('id', shape_id)
        if 'idx' not in st_cxn.attrib:
            st_cxn.set('idx', '0')
        if self._slide_part:
            self._slide_part.save()
        self.reroute()

    @property
    def end_shape_connected_to(self) -> IShape:
        """Returns or sets the shape to attach the end of the connector to. Read/write ."""
        c_nv_cxn_sp_pr = self._get_c_nv_cxn_sp_pr()
        if c_nv_cxn_sp_pr is None:
            return None
        end_cxn = c_nv_cxn_sp_pr.find(f"{NS.A}endCxn")
        if end_cxn is None:
            return None
        shape_id_str = end_cxn.get('id')
        if shape_id_str is None:
            return None
        return self._find_shape_by_id(int(shape_id_str))

    @end_shape_connected_to.setter
    def end_shape_connected_to(self, value: IShape):
        if value is None:
            c_nv_cxn_sp_pr = self._get_c_nv_cxn_sp_pr()
            if c_nv_cxn_sp_pr is not None:
                end_cxn = c_nv_cxn_sp_pr.find(f"{NS.A}endCxn")
                if end_cxn is not None:
                    c_nv_cxn_sp_pr.remove(end_cxn)
                if self._slide_part:
                    self._slide_part.save()
            return
        c_nv_pr = value._get_c_nv_pr() if hasattr(value, '_get_c_nv_pr') else None
        if c_nv_pr is None:
            return
        shape_id = c_nv_pr.get('id')
        if shape_id is None:
            return
        c_nv_cxn_sp_pr = self._ensure_c_nv_cxn_sp_pr()
        end_cxn = c_nv_cxn_sp_pr.find(f"{NS.A}endCxn")
        if end_cxn is None:
            end_cxn = ET.SubElement(c_nv_cxn_sp_pr, f"{NS.A}endCxn")
        end_cxn.set('id', shape_id)
        if 'idx' not in end_cxn.attrib:
            end_cxn.set('idx', '0')
        if self._slide_part:
            self._slide_part.save()
        self.reroute()

    @property
    def start_shape_connection_site_index(self) -> int:
        """Returns or sets the index of connection site for start shape. Read/write ."""
        c_nv_cxn_sp_pr = self._get_c_nv_cxn_sp_pr()
        if c_nv_cxn_sp_pr is None:
            return 0
        st_cxn = c_nv_cxn_sp_pr.find(f"{NS.A}stCxn")
        if st_cxn is None:
            return 0
        try:
            return int(st_cxn.get('idx', '0'))
        except ValueError:
            return 0

    @start_shape_connection_site_index.setter
    def start_shape_connection_site_index(self, value: int):
        c_nv_cxn_sp_pr = self._ensure_c_nv_cxn_sp_pr()
        st_cxn = c_nv_cxn_sp_pr.find(f"{NS.A}stCxn")
        if st_cxn is None:
            st_cxn = ET.SubElement(c_nv_cxn_sp_pr, f"{NS.A}stCxn")
            st_cxn.set('id', '0')
        st_cxn.set('idx', str(value))
        if self._slide_part:
            self._slide_part.save()
        self.reroute()

    @property
    def end_shape_connection_site_index(self) -> int:
        """Returns or sets the index of connection site for end shape. Read/write ."""
        c_nv_cxn_sp_pr = self._get_c_nv_cxn_sp_pr()
        if c_nv_cxn_sp_pr is None:
            return 0
        end_cxn = c_nv_cxn_sp_pr.find(f"{NS.A}endCxn")
        if end_cxn is None:
            return 0
        try:
            return int(end_cxn.get('idx', '0'))
        except ValueError:
            return 0

    @end_shape_connection_site_index.setter
    def end_shape_connection_site_index(self, value: int):
        c_nv_cxn_sp_pr = self._ensure_c_nv_cxn_sp_pr()
        end_cxn = c_nv_cxn_sp_pr.find(f"{NS.A}endCxn")
        if end_cxn is None:
            end_cxn = ET.SubElement(c_nv_cxn_sp_pr, f"{NS.A}endCxn")
            end_cxn.set('id', '0')
        end_cxn.set('idx', str(value))
        if self._slide_part:
            self._slide_part.save()
        self.reroute()

    @property
    def as_i_geometry_shape(self) -> IGeometryShape:
        return self

    def reroute(self) -> None:
        """Recalculates connector bounding box based on connected shapes."""
        start_shape = self.start_shape_connected_to
        end_shape = self.end_shape_connected_to
        if start_shape is None and end_shape is None:
            return

        start_idx = self.start_shape_connection_site_index
        end_idx = self.end_shape_connection_site_index

        if start_shape is not None:
            sx, sy = self._get_connection_point(start_shape, start_idx)
        else:
            sx, sy = self.x, self.y

        if end_shape is not None:
            ex, ey = self._get_connection_point(end_shape, end_idx)
        else:
            ex, ey = self.x + self.width, self.y + self.height

        new_x = min(sx, ex)
        new_y = min(sy, ey)
        new_w = abs(ex - sx)
        new_h = abs(ey - sy)
        flip_h = sx > ex
        flip_v = sy > ey

        xfrm = self._ensure_xfrm()
        off = xfrm.find(Elements.A_OFF)
        if off is None:
            off = ET.SubElement(xfrm, Elements.A_OFF, x="0", y="0")
        ext = xfrm.find(Elements.A_EXT)
        if ext is None:
            ext = ET.SubElement(xfrm, Elements.A_EXT, cx="0", cy="0")

        off.set('x', str(int(round(new_x * EMU_PER_POINT))))
        off.set('y', str(int(round(new_y * EMU_PER_POINT))))
        ext.set('cx', str(int(round(new_w * EMU_PER_POINT))))
        ext.set('cy', str(int(round(new_h * EMU_PER_POINT))))

        if flip_h:
            xfrm.set('flipH', '1')
        elif 'flipH' in xfrm.attrib:
            del xfrm.attrib['flipH']

        if flip_v:
            xfrm.set('flipV', '1')
        elif 'flipV' in xfrm.attrib:
            del xfrm.attrib['flipV']

        if self._slide_part:
            self._slide_part.save()

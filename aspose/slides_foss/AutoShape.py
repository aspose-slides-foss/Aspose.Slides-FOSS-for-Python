from __future__ import annotations
from typing import overload, TYPE_CHECKING
from .GeometryShape import GeometryShape
from .IAutoShape import IAutoShape

if TYPE_CHECKING:
    from .IAdjustValueCollection import IAdjustValueCollection
    from .IGeometryShape import IGeometryShape
    from .ITextFrame import ITextFrame
    from .ShapeType import ShapeType

class AutoShape(GeometryShape, IAutoShape):
    """Represents an AutoShape."""
    # Properties inherited from Shape: hidden, office_interop_shape_id, alternative_text,
    # alternative_text_title, name, slide, presentation


    @property
    def shape_type(self) -> ShapeType:
        from .ShapeType import ShapeType
        from ._internal.pptx.constants import NS
        from ._internal.pptx.shape_type_mapping import ooxml_prst_to_shape_type_name
        if self._xml_element is None:
            return ShapeType.NOT_DEFINED
        sp_pr = self._xml_element.find(f"{NS.P}spPr")
        if sp_pr is None:
            return ShapeType.NOT_DEFINED
        prst_geom = sp_pr.find(f"{NS.A}prstGeom")
        if prst_geom is None:
            cust_geom = sp_pr.find(f"{NS.A}custGeom")
            if cust_geom is not None:
                return ShapeType.CUSTOM
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
        from ._internal.pptx.constants import NS
        from ._internal.pptx.shape_type_mapping import shape_type_name_to_ooxml_prst
        import lxml.etree as ET
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
            cust_geom = sp_pr.find(f"{NS.A}custGeom")
            if cust_geom is not None:
                sp_pr.remove(cust_geom)
            prst_geom = ET.SubElement(sp_pr, f"{NS.A}prstGeom")
        else:
            for child in list(prst_geom):
                prst_geom.remove(child)
        prst_geom.set('prst', prst)
        if self._slide_part:
            self._slide_part.save()



    @property
    def text_frame(self) -> ITextFrame:
        """Returns TextFrame object for the AutoShape. Read-only ."""
        from ._internal.pptx.constants import Elements
        from .TextFrame import TextFrame
        if self._xml_element is None:
            return None
        txbody = self._xml_element.find(Elements.TX_BODY)
        if txbody is None:
            return None
        tf = TextFrame()
        tf._init_internal(txbody, self._slide_part, self._parent_slide, self)
        return tf



    @property
    def is_text_box(self) -> bool:
        """Specifies if the shape is a text box."""
        from ._internal.pptx.constants import Elements
        if self._xml_element is None:
            return False
        return self._xml_element.find(Elements.TX_BODY) is not None

    @property
    def as_i_geometry_shape(self) -> IGeometryShape:
        return self

    def add_text_frame(self, text) -> ITextFrame:
        import lxml.etree as ET
        from ._internal.pptx.constants import Elements
        from .TextFrame import TextFrame
        if self._xml_element is None:
            return None
        # Remove existing txBody if any
        existing = self._xml_element.find(Elements.TX_BODY)
        if existing is not None:
            self._xml_element.remove(existing)
        # Mark shape as text box
        from ._internal.pptx.constants import NS
        nv_sp_pr = self._xml_element.find(f"{NS.P}nvSpPr")
        if nv_sp_pr is not None:
            c_nv_sp_pr = nv_sp_pr.find(f"{NS.P}cNvSpPr")
            if c_nv_sp_pr is not None:
                c_nv_sp_pr.set('txBox', '1')
        # Create new txBody
        txbody = ET.SubElement(self._xml_element, Elements.TX_BODY)
        ET.SubElement(txbody, Elements.A_BODY_PR, rtlCol="0", anchor="ctr")
        ET.SubElement(txbody, Elements.A_LST_STYLE)
        # Split on \r or \n to create separate paragraphs
        import re
        lines = re.split(r'\r\n|\r|\n', text) if text else ['']
        for line in lines:
            p_elem = ET.SubElement(txbody, Elements.A_P)
            ET.SubElement(p_elem, f"{NS.A}pPr", algn="ctr")
            r_elem = ET.SubElement(p_elem, Elements.A_R)
            t_elem = ET.SubElement(r_elem, Elements.A_T)
            t_elem.text = line
        if self._slide_part:
            self._slide_part.save()
        tf = TextFrame()
        tf._init_internal(txbody, self._slide_part, self._parent_slide, self)
        return tf

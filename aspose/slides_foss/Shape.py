from __future__ import annotations
from typing import overload, TYPE_CHECKING, Optional
from abc import ABC, abstractmethod
import lxml.etree as ET
from .IShape import IShape
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent
from .IHyperlinkContainer import IHyperlinkContainer
from ._internal.pptx.constants import NS, Elements, EMU_PER_POINT, ROTATION_UNIT

if TYPE_CHECKING:
    from .IBaseSlide import IBaseSlide
    from .IEffectFormat import IEffectFormat
    from .IFillFormat import IFillFormat
    from .IImage import IImage
    from .ILineFormat import ILineFormat
    from .IPresentation import IPresentation
    from .IShapeFrame import IShapeFrame
    from .IThreeDFormat import IThreeDFormat
    from ._internal.pptx.slide_part import SlidePart

class Shape(IShape, ISlideComponent, IPresentationComponent, IHyperlinkContainer, ABC):
    """Represents a shape on a slide. This is an abstract base class."""

    def __init__(self):
        """Initialize an empty shape."""
        self._xml_element: Optional[ET._Element] = None
        self._slide_part: Optional[SlidePart] = None
        self._parent_slide = None

    def _init_internal(self, xml_element: ET._Element, slide_part: SlidePart, parent_slide) -> None:
        """
        Internal initialization with XML element.

        Args:
            xml_element: The XML element representing this shape.
            slide_part: The SlidePart containing the slide XML.
            parent_slide: The parent Slide object.
        """
        self._xml_element = xml_element
        self._slide_part = slide_part
        self._parent_slide = parent_slide



    def _build_frame(self) -> IShapeFrame:
        """Build a ShapeFrame from the current xfrm element."""
        from .ShapeFrame import ShapeFrame
        from .NullableBool import NullableBool
        xfrm = self._get_xfrm()
        if xfrm is None:
            return ShapeFrame(0, 0, 0, 0, NullableBool.NOT_DEFINED, NullableBool.NOT_DEFINED, 0)
        off = xfrm.find(Elements.A_OFF)
        ext = xfrm.find(Elements.A_EXT)
        x_val = int(off.get('x', '0')) / EMU_PER_POINT if off is not None else 0.0
        y_val = int(off.get('y', '0')) / EMU_PER_POINT if off is not None else 0.0
        w_val = int(ext.get('cx', '0')) / EMU_PER_POINT if ext is not None else 0.0
        h_val = int(ext.get('cy', '0')) / EMU_PER_POINT if ext is not None else 0.0
        rot = int(xfrm.get('rot', '0')) / ROTATION_UNIT
        flip_h_val = NullableBool.TRUE if xfrm.get('flipH') == '1' else NullableBool.FALSE
        flip_v_val = NullableBool.TRUE if xfrm.get('flipV') == '1' else NullableBool.FALSE
        return ShapeFrame(x_val, y_val, w_val, h_val, flip_h_val, flip_v_val, rot)

    def _apply_frame(self, value: IShapeFrame) -> None:
        """Apply a ShapeFrame's values to the xfrm element."""
        from .NullableBool import NullableBool
        xfrm = self._ensure_xfrm()
        off = xfrm.find(Elements.A_OFF)
        if off is None:
            off = ET.SubElement(xfrm, Elements.A_OFF, x="0", y="0")
        ext = xfrm.find(Elements.A_EXT)
        if ext is None:
            ext = ET.SubElement(xfrm, Elements.A_EXT, cx="0", cy="0")
        off.set('x', str(int(round(value.x * EMU_PER_POINT))))
        off.set('y', str(int(round(value.y * EMU_PER_POINT))))
        ext.set('cx', str(int(round(value.width * EMU_PER_POINT))))
        ext.set('cy', str(int(round(value.height * EMU_PER_POINT))))
        xfrm.set('rot', str(int(round(value.rotation * ROTATION_UNIT))))
        if hasattr(value, 'flip_h') and value.flip_h == NullableBool.TRUE:
            xfrm.set('flipH', '1')
        elif 'flipH' in xfrm.attrib:
            del xfrm.attrib['flipH']
        if hasattr(value, 'flip_v') and value.flip_v == NullableBool.TRUE:
            xfrm.set('flipV', '1')
        elif 'flipV' in xfrm.attrib:
            del xfrm.attrib['flipV']
        if self._slide_part:
            self._slide_part.save()

    @property
    def raw_frame(self) -> IShapeFrame:
        """Returns or sets the raw shape frame's properties. Read/write ."""
        return self._build_frame()

    @raw_frame.setter
    def raw_frame(self, value: IShapeFrame):
        self._apply_frame(value)

    @property
    def frame(self) -> IShapeFrame:
        """Returns or sets the shape frame's properties. Read/write ."""
        return self._build_frame()

    @frame.setter
    def frame(self, value: IShapeFrame):
        self._apply_frame(value)

    def _get_sp_pr(self) -> ET._Element | None:
        """Get the spPr (or grpSpPr) element for this shape."""
        if self._xml_element is None:
            return None
        sp_pr = self._xml_element.find(f"{NS.P}spPr")
        if sp_pr is not None:
            return sp_pr
        return self._xml_element.find(f"{NS.P}grpSpPr")

    def _ensure_sp_pr(self) -> ET._Element:
        """Get or create the spPr element."""
        sp_pr = self._get_sp_pr()
        if sp_pr is not None:
            return sp_pr
        if self._xml_element is None:
            raise RuntimeError("Shape has no XML element")
        return ET.SubElement(self._xml_element, f"{NS.P}spPr")

    @property
    def line_format(self) -> ILineFormat:
        """Returns the LineFormat object that contains line formatting properties for a shape. Note: can return null for certain types of shapes which don't have line properties. Read-only ."""
        if self._xml_element is None:
            return None
        from .LineFormat import LineFormat
        sp_pr = self._ensure_sp_pr()
        lf = LineFormat()
        lf._init_internal(sp_pr, self._slide_part, self._parent_slide)
        return lf

    @property
    def three_d_format(self) -> IThreeDFormat:
        """Returns the ThreeDFormat object that 3d effect properties for a shape. Note: can return null for certain types of shapes which don't have 3d properties. Read-only ."""
        if self._xml_element is None:
            return None
        from .ThreeDFormat import ThreeDFormat
        sp_pr = self._ensure_sp_pr()
        tdf = ThreeDFormat()
        tdf._init_internal(sp_pr, self._slide_part, self._parent_slide)
        return tdf

    @property
    def effect_format(self) -> IEffectFormat:
        """Returns the EffectFormat object which contains pixel effects applied to a shape. Note: can return null for certain types of shapes which don't have effect properties. Read-only ."""
        if self._xml_element is None:
            return None
        from .EffectFormat import EffectFormat
        sp_pr = self._ensure_sp_pr()
        ef = EffectFormat()
        ef._init_internal(sp_pr, self._slide_part, self._parent_slide)
        return ef

    @property
    def fill_format(self) -> IFillFormat:
        """Returns the FillFormat object that contains fill formatting properties for a shape. Note: can return null for certain types of shapes which don't have fill properties. Read-only ."""
        if self._xml_element is None:
            return None
        from .FillFormat import FillFormat
        sp_pr = self._ensure_sp_pr()
        ff = FillFormat()
        ff._init_internal(sp_pr, self._slide_part, self._parent_slide)
        return ff






    @property
    def hidden(self) -> bool:
        """Determines whether the shape is hidden. Read/write ."""
        c_nv_pr = self._get_c_nv_pr()
        if c_nv_pr is not None:
            hidden = c_nv_pr.get('hidden')
            return hidden == '1' if hidden else False
        return False

    @hidden.setter
    def hidden(self, value: bool):
        c_nv_pr = self._get_c_nv_pr()
        if c_nv_pr is not None:
            if value:
                c_nv_pr.set('hidden', '1')
            else:
                if 'hidden' in c_nv_pr.attrib:
                    del c_nv_pr.attrib['hidden']
            if self._slide_part:
                self._slide_part.save()

    @property
    def z_order_position(self) -> int:
        """Returns the position of a shape in the z-order. Shapes[0] returns the shape at the back of the z-order, and Shapes[Shapes.Count - 1] returns the shape at the front of the z-order. Read-only ."""
        if self._xml_element is not None:
            parent = self._xml_element.getparent()
            if parent is not None:
                for i, child in enumerate(parent):
                    if child is self._xml_element:
                        return i
        return 0

    @property
    def connection_site_count(self) -> int:
        """Returns the number of connection sites on the shape. Read-only ."""
        # Connection sites use an 8-site model (cardinal + ordinal directions,
        # counter-clockwise from top): 0=top, 1=top-left, 2=left, 3=bottom-left,
        # 4=bottom, 5=bottom-right, 6=right, 7=top-right.
        # Shapes without geometry (e.g., group shapes, graphic frames) have 0.
        if self._xml_element is None:
            return 0
        sp_pr = self._xml_element.find(f"{NS.P}spPr")
        if sp_pr is not None:
            prst_geom = sp_pr.find(f"{NS.A}prstGeom")
            if prst_geom is not None:
                return 8
        return 0

    @property
    def rotation(self) -> float:
        """Returns or sets the number of degrees the specified shape is rotated around the z-axis. A positive value indicates clockwise rotation; a negative value indicates counterclockwise rotation. Read/write ."""
        xfrm = self._get_xfrm()
        if xfrm is not None:
            rot = xfrm.get('rot')
            if rot is not None:
                return int(rot) / ROTATION_UNIT
        return 0.0

    @rotation.setter
    def rotation(self, value: float):
        xfrm = self._ensure_xfrm()
        xfrm.set('rot', str(int(round(value * ROTATION_UNIT))))
        if self._slide_part:
            self._slide_part.save()

    @property
    def x(self) -> float:
        """Gets or sets the x-coordinate of the shape's upper-left corner, measured in points. Read/write ."""
        xfrm = self._get_xfrm()
        if xfrm is not None:
            off = xfrm.find(Elements.A_OFF)
            if off is not None:
                return int(off.get('x', '0')) / EMU_PER_POINT
        return 0.0

    @x.setter
    def x(self, value: float):
        xfrm = self._ensure_xfrm()
        off = xfrm.find(Elements.A_OFF)
        if off is None:
            off = ET.SubElement(xfrm, Elements.A_OFF, x="0", y="0")
        off.set('x', str(int(round(value * EMU_PER_POINT))))
        if self._slide_part:
            self._slide_part.save()

    @property
    def y(self) -> float:
        """Gets or sets the y-coordinate of the shape's upper-left corner, measured in points. Read/write ."""
        xfrm = self._get_xfrm()
        if xfrm is not None:
            off = xfrm.find(Elements.A_OFF)
            if off is not None:
                return int(off.get('y', '0')) / EMU_PER_POINT
        return 0.0

    @y.setter
    def y(self, value: float):
        xfrm = self._ensure_xfrm()
        off = xfrm.find(Elements.A_OFF)
        if off is None:
            off = ET.SubElement(xfrm, Elements.A_OFF, x="0", y="0")
        off.set('y', str(int(round(value * EMU_PER_POINT))))
        if self._slide_part:
            self._slide_part.save()

    @property
    def width(self) -> float:
        """Gets or sets the width of the shape, measured in points. Read/write ."""
        xfrm = self._get_xfrm()
        if xfrm is not None:
            ext = xfrm.find(Elements.A_EXT)
            if ext is not None:
                return int(ext.get('cx', '0')) / EMU_PER_POINT
        return 0.0

    @width.setter
    def width(self, value: float):
        xfrm = self._ensure_xfrm()
        ext = xfrm.find(Elements.A_EXT)
        if ext is None:
            ext = ET.SubElement(xfrm, Elements.A_EXT, cx="0", cy="0")
        ext.set('cx', str(int(round(value * EMU_PER_POINT))))
        if self._slide_part:
            self._slide_part.save()

    @property
    def height(self) -> float:
        """Gets or sets the height of the shape, measured in points. Read/write ."""
        xfrm = self._get_xfrm()
        if xfrm is not None:
            ext = xfrm.find(Elements.A_EXT)
            if ext is not None:
                return int(ext.get('cy', '0')) / EMU_PER_POINT
        return 0.0

    @height.setter
    def height(self, value: float):
        xfrm = self._ensure_xfrm()
        ext = xfrm.find(Elements.A_EXT)
        if ext is None:
            ext = ET.SubElement(xfrm, Elements.A_EXT, cx="0", cy="0")
        ext.set('cy', str(int(round(value * EMU_PER_POINT))))
        if self._slide_part:
            self._slide_part.save()



    @property
    def unique_id(self) -> int:
        """Returns an internal, presentation-scoped identifier intended for use by add-ins or other code. Because this value can be reassigned by the user or programmatically, it must not be treated as a persistent unique key. Read-only . See also ."""
        c_nv_pr = self._get_c_nv_pr()
        if c_nv_pr is not None:
            shape_id = c_nv_pr.get('id')
            if shape_id:
                return int(shape_id)
        return 0

    def _get_c_nv_pr(self) -> Optional[ET._Element]:
        """Get the cNvPr element from the shape XML."""
        if self._xml_element is None:
            return None
        # Different shape types have different structures
        # sp: nvSpPr/cNvPr
        # pic: nvPicPr/cNvPr
        # graphicFrame: nvGraphicFramePr/cNvPr
        # grpSp: nvGrpSpPr/cNvPr
        # cxnSp: nvCxnSpPr/cNvPr
        for nv_elem_name in [f"{NS.P}nvSpPr", f"{NS.P}nvPicPr", f"{NS.P}nvGraphicFramePr",
                             f"{NS.P}nvGrpSpPr", f"{NS.P}nvCxnSpPr"]:
            nv_elem = self._xml_element.find(nv_elem_name)
            if nv_elem is not None:
                return nv_elem.find(Elements.C_NV_PR)
        return None

    @staticmethod
    def _find_xfrm_in_element(xml_element: ET._Element) -> Optional[ET._Element]:
        """Find the a:xfrm element directly within a shape XML element."""
        # Try spPr (most common: sp, pic, cxnSp)
        sp_pr = xml_element.find(f"{NS.P}spPr")
        if sp_pr is not None:
            xfrm = sp_pr.find(Elements.A_XFRM)
            if xfrm is not None:
                return xfrm
        # Try grpSpPr (group shapes)
        grp_sp_pr = xml_element.find(f"{NS.P}grpSpPr")
        if grp_sp_pr is not None:
            xfrm = grp_sp_pr.find(Elements.A_XFRM)
            if xfrm is not None:
                return xfrm
        # Try p:xfrm (graphic frames like tables, charts)
        return xml_element.find(f"{NS.P}xfrm")

    def _get_placeholder_info(self) -> Optional[tuple[Optional[str], str]]:
        """Get (type, idx) from <p:ph> element if this shape is a placeholder."""
        if self._xml_element is None:
            return None
        # Check all nvXxxPr variants for <p:nvPr><p:ph>
        for nv_name in [f"{NS.P}nvSpPr", f"{NS.P}nvPicPr", f"{NS.P}nvGraphicFramePr",
                        f"{NS.P}nvGrpSpPr", f"{NS.P}nvCxnSpPr"]:
            nv_elem = self._xml_element.find(nv_name)
            if nv_elem is not None:
                nv_pr = nv_elem.find(f"{NS.P}nvPr")
                if nv_pr is not None:
                    ph = nv_pr.find(f"{NS.P}ph")
                    if ph is not None:
                        return (ph.get('type'), ph.get('idx', '0'))
        return None

    @staticmethod
    def _find_placeholder_xfrm_in_xml(root: ET._Element, ph_type: Optional[str], ph_idx: str) -> Optional[ET._Element]:
        """Find the xfrm for a matching placeholder in a layout/master XML root."""
        sp_tree = root.find(f".//{Elements.SP_TREE}")
        if sp_tree is None:
            return None
        # Search all shape elements (sp, graphicFrame, etc.)
        for child in sp_tree:
            # Find the nvPr/ph element
            ph = None
            for nv_name in [f"{NS.P}nvSpPr", f"{NS.P}nvPicPr", f"{NS.P}nvGraphicFramePr",
                            f"{NS.P}nvGrpSpPr", f"{NS.P}nvCxnSpPr"]:
                nv_elem = child.find(nv_name)
                if nv_elem is not None:
                    nv_pr = nv_elem.find(f"{NS.P}nvPr")
                    if nv_pr is not None:
                        ph = nv_pr.find(f"{NS.P}ph")
                        break
            if ph is None:
                continue
            # Match by type and idx
            child_type = ph.get('type')
            child_idx = ph.get('idx', '0')
            if child_type == ph_type and child_idx == ph_idx:
                xfrm = Shape._find_xfrm_in_element(child)
                if xfrm is not None:
                    return xfrm
        return None

    def _get_inherited_xfrm(self) -> Optional[ET._Element]:
        """Walk the layout -> master chain to find inherited xfrm for placeholders."""
        ph_info = self._get_placeholder_info()
        if ph_info is None or self._slide_part is None:
            return None
        ph_type, ph_idx = ph_info
        package = self._slide_part._package

        # Try layout slide
        layout_part_name = self._slide_part.layout_part_name
        if layout_part_name:
            layout_content = package.get_part(layout_part_name)
            if layout_content:
                layout_root = ET.fromstring(layout_content)
                xfrm = Shape._find_placeholder_xfrm_in_xml(layout_root, ph_type, ph_idx)
                if xfrm is not None:
                    return xfrm

                # Try master slide (resolve from layout's relationships)
                from ._internal.pptx.layout_slide_part import LayoutSlidePart
                layout_part = LayoutSlidePart(package, layout_part_name)
                master_part_name = layout_part.master_part_name
                if master_part_name:
                    master_content = package.get_part(master_part_name)
                    if master_content:
                        master_root = ET.fromstring(master_content)
                        xfrm = Shape._find_placeholder_xfrm_in_xml(master_root, ph_type, ph_idx)
                        if xfrm is not None:
                            return xfrm
        return None

    def _get_xfrm(self) -> Optional[ET._Element]:
        """Get the a:xfrm element from the shape XML.

        Handles different shape types:
        - sp, pic, cxnSp: spPr/a:xfrm
        - grpSp: grpSpPr/a:xfrm
        - graphicFrame: p:xfrm (direct child)

        For placeholder shapes with no local xfrm, walks the
        layout -> master inheritance chain.
        """
        if self._xml_element is None:
            return None
        xfrm = Shape._find_xfrm_in_element(self._xml_element)
        if xfrm is not None:
            return xfrm
        # Placeholder inheritance: try layout, then master
        return self._get_inherited_xfrm()

    def _ensure_xfrm(self) -> ET._Element:
        """Get or create the a:xfrm element."""
        xfrm = self._get_xfrm()
        if xfrm is not None:
            return xfrm
        if self._xml_element is None:
            raise RuntimeError("Shape has no XML element")
        # Create xfrm under the appropriate parent
        sp_pr = self._xml_element.find(f"{NS.P}spPr")
        if sp_pr is None:
            grp_sp_pr = self._xml_element.find(f"{NS.P}grpSpPr")
            if grp_sp_pr is not None:
                sp_pr = grp_sp_pr
            else:
                sp_pr = ET.SubElement(self._xml_element, f"{NS.P}spPr")
        xfrm = ET.SubElement(sp_pr, Elements.A_XFRM)
        ET.SubElement(xfrm, Elements.A_OFF, x="0", y="0")
        ET.SubElement(xfrm, Elements.A_EXT, cx="0", cy="0")
        return xfrm

    @property
    def office_interop_shape_id(self) -> int:
        """Returns a slide-scoped unique identifier that remains constant for the lifetime of the shape and lets PowerPoint or interop code reliably reference the shape from anywhere in the document. Read-only . See also ."""
        c_nv_pr = self._get_c_nv_pr()
        if c_nv_pr is not None:
            shape_id = c_nv_pr.get('id')
            if shape_id:
                return int(shape_id)
        return 0

    @property
    def alternative_text(self) -> str:
        """Returns or sets the alternative text associated with a shape. Read/write ."""
        c_nv_pr = self._get_c_nv_pr()
        if c_nv_pr is not None:
            descr = c_nv_pr.get('descr')
            return descr if descr else ''
        return ''

    @alternative_text.setter
    def alternative_text(self, value: str):
        c_nv_pr = self._get_c_nv_pr()
        if c_nv_pr is not None:
            c_nv_pr.set('descr', value)
            if self._slide_part:
                self._slide_part.save()

    @property
    def alternative_text_title(self) -> str:
        """Returns or sets the title of alternative text associated with a shape. Read/write ."""
        c_nv_pr = self._get_c_nv_pr()
        if c_nv_pr is not None:
            title = c_nv_pr.get('title')
            return title if title else ''
        return ''

    @alternative_text_title.setter
    def alternative_text_title(self, value: str):
        c_nv_pr = self._get_c_nv_pr()
        if c_nv_pr is not None:
            c_nv_pr.set('title', value)
            if self._slide_part:
                self._slide_part.save()

    @property
    def name(self) -> str:
        """Returns or sets the name of a shape. Must be not null. Use empty string value if needed. Read/write ."""
        c_nv_pr = self._get_c_nv_pr()
        if c_nv_pr is not None:
            name = c_nv_pr.get('name')
            return name if name else ''
        return ''

    @name.setter
    def name(self, value: str):
        c_nv_pr = self._get_c_nv_pr()
        if c_nv_pr is not None:
            c_nv_pr.set('name', value)
            if self._slide_part:
                self._slide_part.save()

    _DECORATIVE_URI = '{http://schemas.microsoft.com/office/drawing/2017/decorative}'

    @property
    def is_decorative(self) -> bool:
        """Gets or sets 'Mark as decorative' option Reed/write ."""
        c_nv_pr = self._get_c_nv_pr()
        if c_nv_pr is None:
            return False
        ext_lst = c_nv_pr.find(f"{NS.A}extLst")
        if ext_lst is None:
            return False
        for ext in ext_lst.findall(f"{NS.A}ext"):
            decorative = ext.find(f"{self._DECORATIVE_URI}decorative")
            if decorative is not None:
                return decorative.get('val', '0') == '1'
        return False

    @is_decorative.setter
    def is_decorative(self, value: bool):
        c_nv_pr = self._get_c_nv_pr()
        if c_nv_pr is None:
            return
        ext_lst = c_nv_pr.find(f"{NS.A}extLst")
        if ext_lst is None:
            ext_lst = ET.SubElement(c_nv_pr, f"{NS.A}extLst")
        # Find existing decorative extension
        dec_ext = None
        for ext in ext_lst.findall(f"{NS.A}ext"):
            if ext.find(f"{self._DECORATIVE_URI}decorative") is not None:
                dec_ext = ext
                break
        if dec_ext is None:
            dec_ext = ET.SubElement(ext_lst, f"{NS.A}ext",
                                   uri='{C183D7F6-B498-43B3-948B-1728B52AA6E4}')
        decorative = dec_ext.find(f"{self._DECORATIVE_URI}decorative")
        if decorative is None:
            decorative = ET.SubElement(dec_ext, f"{self._DECORATIVE_URI}decorative")
        decorative.set('val', '1' if value else '0')
        if self._slide_part:
            self._slide_part.save()


    @property
    def is_grouped(self) -> bool:
        """Determines whether the shape is grouped. Read-only ."""
        if self._xml_element is not None:
            parent = self._xml_element.getparent()
            if parent is not None:
                return parent.tag == f"{NS.P}grpSp"
        return False


    @property
    def slide(self) -> IBaseSlide:
        """Returns the parent slide of a shape. Read-only ."""
        return self._parent_slide

    @property
    def presentation(self) -> IPresentation:
        """Returns the parent presentation of a slide. Read-only ."""
        if self._parent_slide and hasattr(self._parent_slide, 'presentation'):
            return self._parent_slide.presentation
        return None


    @property
    def as_i_slide_component(self) -> ISlideComponent:
        return self

    @property
    def as_i_presentation_component(self) -> IPresentationComponent:
        return self











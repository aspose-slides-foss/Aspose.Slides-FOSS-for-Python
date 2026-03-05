from __future__ import annotations
from typing import overload, TYPE_CHECKING, Any, Optional
import lxml.etree as ET
from .IShapeCollection import IShapeCollection
from ._internal.pptx.constants import NS, Elements

if TYPE_CHECKING:
    from .IAutoShape import IAutoShape
    from .IConnector import IConnector
    from .IPictureFrame import IPictureFrame
    from .IShape import IShape
    from .ITable import ITable
    from .Shape import Shape
    from ._internal.pptx.slide_part import SlidePart

# Default adjustment values (name, val) for connector preset types.
# Connectors with no entries have zero adjustments and use an empty avLst.
_CONNECTOR_DEFAULT_ADJUSTMENTS: dict[str, list[tuple[str, int]]] = {
    'straightConnector1': [],
    'bentConnector2':     [],
    'bentConnector3':     [('adj1', 50000)],
    'bentConnector4':     [('adj1', 50000), ('adj2', 50000)],
    'bentConnector5':     [('adj1', 50000), ('adj2', 50000), ('adj3', 50000)],
    'curvedConnector2':   [],
    'curvedConnector3':   [('adj1', 50000)],
    'curvedConnector4':   [('adj1', 50000), ('adj2', 50000)],
    'curvedConnector5':   [('adj1', 50000), ('adj2', 50000), ('adj3', 50000)],
}


from ._internal.base_collection import BaseCollection
class ShapeCollection(BaseCollection, IShapeCollection):
    """Represents a collection of shapes."""

    def __init__(self):
        """Initialize an empty shape collection."""
        self._slide_part: Optional[SlidePart] = None
        self._parent_slide = None
        self._shapes_cache: Optional[list[IShape]] = None
        # Maps id(xml_element) -> shape object so that the same element always
        # returns the same Python wrapper (preserves `is` identity).
        self._element_to_shape: dict = {}

    def _init_internal(self, slide_part: SlidePart, parent_slide) -> None:
        """
        Internal initialization with slide part.

        Args:
            slide_part: The SlidePart containing the slide XML.
            parent_slide: The parent Slide object.
        """
        self._slide_part = slide_part
        self._parent_slide = parent_slide
        self._shapes_cache = None
        self._element_to_shape = {}

    def _get_sp_tree(self) -> Optional[ET._Element]:
        """Get the spTree element from the slide XML."""
        if self._slide_part is None or self._slide_part._root is None:
            return None
        return self._slide_part._root.find(f".//{Elements.SP_TREE}")

    def _load_shapes(self) -> list[IShape]:
        """Load all shapes from the XML."""
        if self._shapes_cache is not None:
            return self._shapes_cache

        shapes = []
        sp_tree = self._get_sp_tree()
        if sp_tree is None:
            return shapes

        # Import shape factory here to avoid circular imports
        from ._internal.pptx.shape_factory import create_shape

        # Iterate through all shape elements in order
        # Handle different shape types: sp (shape), pic (picture), graphicFrame (chart/table),
        # grpSp (group), cxnSp (connector)
        for elem in sp_tree:
            tag = elem.tag

            # Skip the group shape properties (nvGrpSpPr and grpSpPr)
            if tag in (f"{NS.P}nvGrpSpPr", f"{NS.P}grpSpPr"):
                continue

            # Check if this is a shape element we should include
            if tag in (Elements.SP, f"{NS.P}pic", f"{NS.P}graphicFrame",
                      f"{NS.P}grpSp", f"{NS.P}cxnSp"):
                # Reuse existing wrapper if available to preserve Python identity
                elem_key = id(elem)
                if elem_key in self._element_to_shape:
                    shape = self._element_to_shape[elem_key]
                else:
                    shape = create_shape(elem, self._slide_part, self._parent_slide)
                    if shape is not None:
                        self._element_to_shape[elem_key] = shape
                if shape is not None:
                    shapes.append(shape)

        self._shapes_cache = shapes
        return shapes

    def _invalidate_cache(self) -> None:
        """Invalidate the shapes cache when the collection changes."""
        self._shapes_cache = None

    def _save(self) -> None:
        """Save changes to the slide part."""
        if self._slide_part:
            self._slide_part.save()

    def _next_shape_id(self) -> int:
        """Find the next available shape ID in the spTree."""
        sp_tree = self._get_sp_tree()
        if sp_tree is None:
            return 2
        max_id = 1
        for elem in sp_tree.iter():
            id_val = elem.get('id')
            if id_val is not None:
                try:
                    max_id = max(max_id, int(id_val))
                except ValueError:
                    pass
        return max_id + 1

    def _build_auto_shape_xml(self, shape_id: int, name: str, shape_type, x: float, y: float,
                              width: float, height: float, create_from_template: bool) -> ET._Element:
        """Build XML for a new AutoShape element."""
        from ._internal.pptx.constants import EMU_PER_POINT
        from ._internal.pptx.shape_type_mapping import shape_type_name_to_ooxml_prst

        prst = shape_type_name_to_ooxml_prst(shape_type.name)
        if prst is None:
            prst = 'rect'

        x_emu = str(int(round(x * EMU_PER_POINT)))
        y_emu = str(int(round(y * EMU_PER_POINT)))
        w_emu = str(int(round(width * EMU_PER_POINT)))
        h_emu = str(int(round(height * EMU_PER_POINT)))

        sp = ET.Element(Elements.SP)

        # nvSpPr
        nv_sp_pr = ET.SubElement(sp, Elements.NV_SP_PR)
        c_nv_pr = ET.SubElement(nv_sp_pr, Elements.C_NV_PR)
        c_nv_pr.set('id', str(shape_id))
        c_nv_pr.set('name', name)
        ET.SubElement(nv_sp_pr, f"{NS.P}cNvSpPr")
        ET.SubElement(nv_sp_pr, f"{NS.P}nvPr")

        # spPr
        sp_pr = ET.SubElement(sp, Elements.SP_PR)
        xfrm = ET.SubElement(sp_pr, f"{NS.A}xfrm")
        off = ET.SubElement(xfrm, f"{NS.A}off")
        off.set('x', x_emu)
        off.set('y', y_emu)
        ext = ET.SubElement(xfrm, f"{NS.A}ext")
        ext.set('cx', w_emu)
        ext.set('cy', h_emu)
        prst_geom = ET.SubElement(sp_pr, f"{NS.A}prstGeom", prst=prst)
        ET.SubElement(prst_geom, f"{NS.A}avLst")

        if create_from_template:
            # Add p:style for theme-based appearance (fill, line, effects, font color)
            # Must come before txBody per OOXML element ordering
            style = ET.SubElement(sp, f"{NS.P}style")
            ln_ref = ET.SubElement(style, f"{NS.A}lnRef", idx="2")
            ln_ref_clr = ET.SubElement(ln_ref, f"{NS.A}schemeClr", val="accent1")
            ET.SubElement(ln_ref_clr, f"{NS.A}shade", val="50000")
            fill_ref = ET.SubElement(style, f"{NS.A}fillRef", idx="1")
            ET.SubElement(fill_ref, f"{NS.A}schemeClr", val="accent1")
            effect_ref = ET.SubElement(style, f"{NS.A}effectRef", idx="0")
            ET.SubElement(effect_ref, f"{NS.A}schemeClr", val="accent1")
            font_ref = ET.SubElement(style, f"{NS.A}fontRef", idx="minor")
            ET.SubElement(font_ref, f"{NS.A}schemeClr", val="lt1")

        # txBody - must come after p:style per OOXML element ordering
        tx_body = ET.SubElement(sp, f"{NS.P}txBody")
        ET.SubElement(tx_body, f"{NS.A}bodyPr", rtlCol="0", anchor="ctr")
        ET.SubElement(tx_body, f"{NS.A}lstStyle")
        a_p = ET.SubElement(tx_body, f"{NS.A}p")
        ET.SubElement(a_p, f"{NS.A}endParaRPr")

        return sp

    def _build_connector_xml(self, shape_id: int, name: str, shape_type, x: float, y: float,
                             width: float, height: float, create_from_template: bool) -> ET._Element:
        """Build XML for a new connector (cxnSp) element."""
        from ._internal.pptx.constants import EMU_PER_POINT
        from ._internal.pptx.shape_type_mapping import shape_type_name_to_ooxml_prst

        prst = shape_type_name_to_ooxml_prst(shape_type.name)
        if prst is None:
            prst = 'bentConnector3'

        x_emu = str(int(round(x * EMU_PER_POINT)))
        y_emu = str(int(round(y * EMU_PER_POINT)))
        w_emu = str(int(round(width * EMU_PER_POINT)))
        h_emu = str(int(round(height * EMU_PER_POINT)))

        cxn_sp = ET.Element(f"{NS.P}cxnSp")

        # nvCxnSpPr
        nv_cxn_sp_pr = ET.SubElement(cxn_sp, f"{NS.P}nvCxnSpPr")
        c_nv_pr = ET.SubElement(nv_cxn_sp_pr, Elements.C_NV_PR)
        c_nv_pr.set('id', str(shape_id))
        c_nv_pr.set('name', name)
        ET.SubElement(nv_cxn_sp_pr, f"{NS.P}cNvCxnSpPr")
        ET.SubElement(nv_cxn_sp_pr, f"{NS.P}nvPr")

        # spPr
        sp_pr = ET.SubElement(cxn_sp, Elements.SP_PR)
        xfrm = ET.SubElement(sp_pr, f"{NS.A}xfrm")
        off = ET.SubElement(xfrm, f"{NS.A}off")
        off.set('x', x_emu)
        off.set('y', y_emu)
        ext = ET.SubElement(xfrm, f"{NS.A}ext")
        ext.set('cx', w_emu)
        ext.set('cy', h_emu)
        prst_geom = ET.SubElement(sp_pr, f"{NS.A}prstGeom", prst=prst)
        av_lst = ET.SubElement(prst_geom, f"{NS.A}avLst")
        for adj_name, adj_val in _CONNECTOR_DEFAULT_ADJUSTMENTS.get(prst, []):
            gd = ET.SubElement(av_lst, f"{NS.A}gd")
            gd.set('name', adj_name)
            gd.set('fmla', f'val {adj_val}')

        if create_from_template:
            style = ET.SubElement(cxn_sp, f"{NS.P}style")
            ln_ref = ET.SubElement(style, f"{NS.A}lnRef", idx="1")
            ET.SubElement(ln_ref, f"{NS.A}schemeClr", val="accent1")
            fill_ref = ET.SubElement(style, f"{NS.A}fillRef", idx="0")
            ET.SubElement(fill_ref, f"{NS.A}schemeClr", val="accent1")
            effect_ref = ET.SubElement(style, f"{NS.A}effectRef", idx="0")
            ET.SubElement(effect_ref, f"{NS.A}schemeClr", val="accent1")
            font_ref = ET.SubElement(style, f"{NS.A}fontRef", idx="minor")
            ET.SubElement(font_ref, f"{NS.A}schemeClr", val="tx1")

        return cxn_sp

    def _add_connector_impl(self, index, shape_type, x: float, y: float,
                            width: float, height: float, create_from_template: bool) -> IConnector:
        """Core implementation for add_connector and insert_connector."""
        from .Connector import Connector

        sp_tree = self._get_sp_tree()
        if sp_tree is None:
            raise RuntimeError("Cannot add shape: slide has no shape tree")

        shape_id = self._next_shape_id()
        name = f"Connector {shape_id}"

        cxn_xml = self._build_connector_xml(shape_id, name, shape_type, x, y, width, height, create_from_template)

        if index is None:
            sp_tree.append(cxn_xml)
        else:
            shape_count = 0
            insert_pos = len(sp_tree)
            for i, elem in enumerate(sp_tree):
                tag = elem.tag
                if tag in (f"{NS.P}nvGrpSpPr", f"{NS.P}grpSpPr"):
                    continue
                if shape_count == index:
                    insert_pos = i
                    break
                shape_count += 1
            sp_tree.insert(insert_pos, cxn_xml)

        self._invalidate_cache()
        self._save()

        connector = Connector()
        connector._init_internal(cxn_xml, self._slide_part, self._parent_slide)
        self._element_to_shape[id(cxn_xml)] = connector
        return connector

    def _add_auto_shape_impl(self, index, shape_type, x: float, y: float,
                             width: float, height: float, create_from_template: bool) -> IAutoShape:
        """Core implementation for add_auto_shape and insert_auto_shape."""
        from .AutoShape import AutoShape
        from ._internal.pptx.shape_factory import create_shape

        sp_tree = self._get_sp_tree()
        if sp_tree is None:
            raise RuntimeError("Cannot add shape: slide has no shape tree")

        shape_id = self._next_shape_id()
        name = f"{shape_type.name.replace('_', ' ').title()} {shape_id}"

        sp_xml = self._build_auto_shape_xml(shape_id, name, shape_type, x, y, width, height, create_from_template)

        if index is None:
            sp_tree.append(sp_xml)
        else:
            # Find the correct XML insertion point (skip nvGrpSpPr and grpSpPr)
            shape_count = 0
            insert_pos = len(sp_tree)
            for i, elem in enumerate(sp_tree):
                tag = elem.tag
                if tag in (f"{NS.P}nvGrpSpPr", f"{NS.P}grpSpPr"):
                    continue
                if shape_count == index:
                    insert_pos = i
                    break
                shape_count += 1
            sp_tree.insert(insert_pos, sp_xml)

        self._invalidate_cache()
        self._save()

        shape = AutoShape()
        shape._init_internal(sp_xml, self._slide_part, self._parent_slide)
        self._element_to_shape[id(sp_xml)] = shape
        return shape

    def __len__(self) -> int:
        """Return the number of shapes in the collection."""
        return len(self._load_shapes())

    def __iter__(self):
        """Iterate over shapes in the collection."""
        return iter(self._load_shapes())

    @property
    def parent_group(self) -> IGroupShape:
        """Gets the parent group shape object for the shapes collection. Read-only ."""
        # For slide-level shapes, there's no parent group
        return None

    @property
    def as_i_collection(self) -> list:
        return self._load_shapes()

    @property
    def as_i_enumerable(self) -> Any:
        return self._load_shapes()




































    def to_array(self, *args, **kwargs) -> list[IShape]:
        """Convert the collection to an array."""
        shapes = self._load_shapes()
        if len(args) == 0:
            return list(shapes)
        elif len(args) == 2:
            start_index = args[0]
            count = args[1]
            return list(shapes[start_index:start_index + count])
        else:
            raise ValueError("Unsupported arguments for this method.")



    def reorder(self, *args, **kwargs) -> None:
        """Reorder shapes in the collection."""
        if len(args) != 2:
            raise ValueError("Unsupported arguments for this method.")

        new_index = args[0]
        shape_or_shapes = args[1]

        # Check if it's a single shape or a list of shapes
        if isinstance(shape_or_shapes, list):
            # Multiple shapes
            for shape in shape_or_shapes:
                self._reorder_single(new_index, shape)
                new_index += 1
        else:
            # Single shape
            self._reorder_single(new_index, shape_or_shapes)

        self._invalidate_cache()
        self._save()

    def _reorder_single(self, new_index: int, shape: IShape) -> None:
        """Reorder a single shape to a new position."""
        sp_tree = self._get_sp_tree()
        if sp_tree is None:
            return

        # Find the shape's XML element
        shape_elem = shape._xml_element if hasattr(shape, '_xml_element') else None
        if shape_elem is None or shape_elem not in sp_tree:
            return

        # Remove the shape from its current position
        sp_tree.remove(shape_elem)

        # Find the correct insertion point (skip nvGrpSpPr and grpSpPr)
        insert_position = 0
        current_shape_index = -1
        for i, elem in enumerate(sp_tree):
            tag = elem.tag
            if tag in (f"{NS.P}nvGrpSpPr", f"{NS.P}grpSpPr"):
                insert_position = i + 1
                continue
            current_shape_index += 1
            if current_shape_index >= new_index:
                insert_position = i
                break
        else:
            # Append at the end
            insert_position = len(sp_tree)

        # Insert the shape at the new position
        sp_tree.insert(insert_position, shape_elem)



    def add_auto_shape(self, *args, **kwargs) -> IAutoShape:
        if len(args) >= 5:
            shape_type = args[0]
            x, y, width, height = args[1], args[2], args[3], args[4]
            create_from_template = args[5] if len(args) > 5 else True
            return self._add_auto_shape_impl(None, shape_type, x, y, width, height, create_from_template)
        raise ValueError("Unsupported arguments for this method.")



    def insert_auto_shape(self, *args, **kwargs) -> IAutoShape:
        if len(args) >= 6:
            index = args[0]
            shape_type = args[1]
            x, y, width, height = args[2], args[3], args[4], args[5]
            create_from_template = args[6] if len(args) > 6 else True
            return self._add_auto_shape_impl(index, shape_type, x, y, width, height, create_from_template)
        raise ValueError("Unsupported arguments for this method.")






    def add_connector(self, *args, **kwargs) -> IConnector:
        if len(args) >= 5:
            shape_type = args[0]
            x, y, width, height = args[1], args[2], args[3], args[4]
            create_from_template = args[5] if len(args) > 5 else True
            return self._add_connector_impl(None, shape_type, x, y, width, height, create_from_template)
        raise ValueError("Unsupported arguments for this method.")



    def insert_connector(self, *args, **kwargs) -> IConnector:
        if len(args) >= 6:
            index = args[0]
            shape_type = args[1]
            x, y, width, height = args[2], args[3], args[4], args[5]
            create_from_template = args[6] if len(args) > 6 else True
            return self._add_connector_impl(index, shape_type, x, y, width, height, create_from_template)
        raise ValueError("Unsupported arguments for this method.")

















    def index_of(self, shape: IShape) -> int:
        """Return the zero-based index of the specified shape."""
        shapes = self._load_shapes()
        try:
            return shapes.index(shape)
        except ValueError:
            return -1



    def add_picture_frame(self, shape_type, x, y, width, height, image) -> IPictureFrame:
        return self._add_picture_frame_impl(None, shape_type, x, y, width, height, image)

    def insert_picture_frame(self, index, shape_type, x, y, width, height, image) -> IPictureFrame:
        return self._add_picture_frame_impl(index, shape_type, x, y, width, height, image)

    def _add_picture_frame_impl(self, index, shape_type, x: float, y: float,
                                 width: float, height: float, image) -> IPictureFrame:
        """Core implementation for add_picture_frame and insert_picture_frame."""
        from .PictureFrame import PictureFrame
        from ._internal.pptx.constants import EMU_PER_POINT, NS, Attributes
        from ._internal.pptx.shape_type_mapping import shape_type_name_to_ooxml_prst
        from ._internal.opc.relationships import REL_TYPES

        sp_tree = self._get_sp_tree()
        if sp_tree is None:
            raise RuntimeError("Cannot add shape: slide has no shape tree")

        # Ensure image is in the presentation's image collection
        if not hasattr(image, '_part_name'):
            raise ValueError("Image must be a PPImage from the presentation's image collection")

        image_part_name = image._part_name

        # Add image relationship to slide's .rels
        slide_dir = self._slide_part._part_name.rsplit('/', 1)[0]
        image_parts = image_part_name.split('/')
        slide_parts = slide_dir.split('/')
        # Compute relative path
        common = 0
        for i in range(min(len(slide_parts), len(image_parts))):
            if slide_parts[i] == image_parts[i]:
                common += 1
            else:
                break
        up = len(slide_parts) - common
        remaining = image_parts[common:]
        relative_target = '/'.join(['..'] * up + remaining)

        # Check if relationship already exists
        existing_rels = self._slide_part._rels_manager.get_relationships_by_type(REL_TYPES['image'])
        embed_id = None
        for rel in existing_rels:
            resolved = self._slide_part._resolve_target(rel.target)
            if resolved == image_part_name:
                embed_id = rel.id
                break
        if embed_id is None:
            embed_id = self._slide_part._rels_manager.add_relationship(
                REL_TYPES['image'], relative_target
            )
            self._slide_part._rels_manager.save()

        # Build shape XML
        shape_id = self._next_shape_id()
        name = f"Picture {shape_id}"

        prst = shape_type_name_to_ooxml_prst(shape_type.name)
        if prst is None:
            prst = 'rect'

        x_emu = str(int(round(x * EMU_PER_POINT)))
        y_emu = str(int(round(y * EMU_PER_POINT)))
        w_emu = str(int(round(width * EMU_PER_POINT)))
        h_emu = str(int(round(height * EMU_PER_POINT)))

        pic = ET.Element(f'{NS.P}pic')

        # nvPicPr
        nv_pic_pr = ET.SubElement(pic, f'{NS.P}nvPicPr')
        c_nv_pr = ET.SubElement(nv_pic_pr, Elements.C_NV_PR)
        c_nv_pr.set('id', str(shape_id))
        c_nv_pr.set('name', name)
        c_nv_pic_pr = ET.SubElement(nv_pic_pr, f'{NS.P}cNvPicPr')
        pic_locks = ET.SubElement(c_nv_pic_pr, f'{NS.A}picLocks')
        pic_locks.set('noChangeAspect', '1')
        ET.SubElement(nv_pic_pr, f'{NS.P}nvPr')

        # blipFill
        blip_fill = ET.SubElement(pic, f'{NS.P}blipFill')
        blip = ET.SubElement(blip_fill, f'{NS.A}blip')
        blip.set(Attributes.R_EMBED, embed_id)
        stretch = ET.SubElement(blip_fill, f'{NS.A}stretch')
        ET.SubElement(stretch, f'{NS.A}fillRect')

        # spPr
        sp_pr = ET.SubElement(pic, Elements.SP_PR)
        xfrm = ET.SubElement(sp_pr, f'{NS.A}xfrm')
        off = ET.SubElement(xfrm, f'{NS.A}off')
        off.set('x', x_emu)
        off.set('y', y_emu)
        ext = ET.SubElement(xfrm, f'{NS.A}ext')
        ext.set('cx', w_emu)
        ext.set('cy', h_emu)
        prst_geom = ET.SubElement(sp_pr, f'{NS.A}prstGeom', prst=prst)
        ET.SubElement(prst_geom, f'{NS.A}avLst')

        if index is None:
            sp_tree.append(pic)
        else:
            # Find the correct XML insertion point (skip nvGrpSpPr and grpSpPr)
            shape_count = 0
            insert_pos = len(sp_tree)
            for i, elem in enumerate(sp_tree):
                tag = elem.tag
                if tag in (f"{NS.P}nvGrpSpPr", f"{NS.P}grpSpPr"):
                    continue
                if shape_count == index:
                    insert_pos = i
                    break
                shape_count += 1
            sp_tree.insert(insert_pos, pic)

        self._invalidate_cache()
        self._save()

        picture_frame = PictureFrame()
        picture_frame._init_internal(pic, self._slide_part, self._parent_slide)
        self._element_to_shape[id(pic)] = picture_frame
        return picture_frame

    def add_table(self, x, y, column_widths, row_heights) -> ITable:
        return self._add_table_impl(None, x, y, column_widths, row_heights)

    def insert_table(self, index, x, y, column_widths, row_heights) -> ITable:
        return self._add_table_impl(index, x, y, column_widths, row_heights)

    def _add_table_impl(self, index, x: float, y: float,
                         column_widths: list[float], row_heights: list[float]) -> ITable:
        """Core implementation for add_table and insert_table."""
        from .Table import Table
        from ._internal.pptx.constants import EMU_PER_POINT, Elements

        sp_tree = self._get_sp_tree()
        if sp_tree is None:
            raise RuntimeError("Cannot add shape: slide has no shape tree")

        shape_id = self._next_shape_id()
        name = f"Table {shape_id}"

        x_emu = str(int(round(x * EMU_PER_POINT)))
        y_emu = str(int(round(y * EMU_PER_POINT)))
        total_w = sum(column_widths)
        total_h = sum(row_heights)
        w_emu = str(int(round(total_w * EMU_PER_POINT)))
        h_emu = str(int(round(total_h * EMU_PER_POINT)))

        num_cols = len(column_widths)
        num_rows = len(row_heights)

        # Build the graphicFrame XML
        gf = ET.Element(Elements.P_GRAPHIC_FRAME)

        # nvGraphicFramePr
        nv_gf_pr = ET.SubElement(gf, Elements.P_NV_GRAPHIC_FRAME_PR)
        c_nv_pr = ET.SubElement(nv_gf_pr, Elements.C_NV_PR)
        c_nv_pr.set('id', str(shape_id))
        c_nv_pr.set('name', name)
        c_nv_gf_pr = ET.SubElement(nv_gf_pr, Elements.P_C_NV_GRAPHIC_FRAME_PR)
        gf_locking = ET.SubElement(c_nv_gf_pr, Elements.A_GRAPHIC_FRAME_LOCKING)
        gf_locking.set('noGrp', '1')
        ET.SubElement(nv_gf_pr, Elements.P_NV_PR)

        # p:xfrm
        xfrm = ET.SubElement(gf, Elements.P_XFRM)
        off = ET.SubElement(xfrm, Elements.A_OFF)
        off.set('x', x_emu)
        off.set('y', y_emu)
        ext = ET.SubElement(xfrm, Elements.A_EXT)
        ext.set('cx', w_emu)
        ext.set('cy', h_emu)

        # a:graphic > a:graphicData > a:tbl
        graphic = ET.SubElement(gf, Elements.A_GRAPHIC)
        graphic_data = ET.SubElement(graphic, Elements.A_GRAPHIC_DATA)
        graphic_data.set('uri', Elements.TABLE_URI)

        tbl = ET.SubElement(graphic_data, Elements.A_TBL)

        # a:tblPr with default style
        tbl_pr = ET.SubElement(tbl, Elements.A_TBL_PR)
        tbl_pr.set('firstRow', '1')
        tbl_pr.set('bandRow', '1')
        # Set default table style: MediumStyle2Accent1
        tbl_style_id = ET.SubElement(tbl_pr, Elements.A_TABLE_STYLE_ID)
        tbl_style_id.text = '{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}'

        # a:tblGrid
        tbl_grid = ET.SubElement(tbl, Elements.A_TBL_GRID)
        for cw in column_widths:
            grid_col = ET.SubElement(tbl_grid, Elements.A_GRID_COL)
            grid_col.set('w', str(int(round(cw * EMU_PER_POINT))))

        # Rows
        for rh in row_heights:
            tr = ET.SubElement(tbl, Elements.A_TR)
            tr.set('h', str(int(round(rh * EMU_PER_POINT))))
            for _ in range(num_cols):
                tc = ET.SubElement(tr, Elements.A_TC)
                txbody = ET.SubElement(tc, Elements.A_TX_BODY)
                ET.SubElement(txbody, Elements.A_BODY_PR)
                ET.SubElement(txbody, Elements.A_LST_STYLE)
                ET.SubElement(txbody, Elements.A_P)
                ET.SubElement(tc, Elements.A_TC_PR)

        # Insert into spTree
        if index is None:
            sp_tree.append(gf)
        else:
            shape_count = 0
            insert_pos = len(sp_tree)
            for i, elem in enumerate(sp_tree):
                tag = elem.tag
                if tag in (f"{NS.P}nvGrpSpPr", f"{NS.P}grpSpPr"):
                    continue
                if shape_count == index:
                    insert_pos = i
                    break
                shape_count += 1
            sp_tree.insert(insert_pos, gf)

        self._invalidate_cache()
        self._save()

        table = Table()
        table._init_internal(gf, self._slide_part, self._parent_slide)
        return table

    def remove_at(self, index: int) -> None:
        """Remove the shape at the specified index."""
        shapes = self._load_shapes()
        if index < 0 or index >= len(shapes):
            raise IndexError(f"Index {index} is out of range")

        shape = shapes[index]
        self.remove(shape)

    def remove(self, shape: IShape) -> None:
        """Remove the specified shape from the collection."""
        sp_tree = self._get_sp_tree()
        if sp_tree is None:
            return

        # Get the shape's XML element
        shape_elem = shape._xml_element if hasattr(shape, '_xml_element') else None
        if shape_elem is None:
            raise ValueError("Shape does not have a valid XML element")

        if shape_elem in sp_tree:
            sp_tree.remove(shape_elem)
            self._element_to_shape.pop(id(shape_elem), None)
            self._invalidate_cache()
            self._save()
        else:
            raise ValueError("Shape not found in collection")

    def clear(self) -> None:
        """Remove all shapes from the collection."""
        sp_tree = self._get_sp_tree()
        if sp_tree is None:
            return

        # Remove all shape elements (keep nvGrpSpPr and grpSpPr)
        elements_to_remove = []
        for elem in sp_tree:
            tag = elem.tag
            if tag not in (f"{NS.P}nvGrpSpPr", f"{NS.P}grpSpPr"):
                elements_to_remove.append(elem)

        for elem in elements_to_remove:
            sp_tree.remove(elem)

        self._invalidate_cache()
        self._save()

    def __getitem__(self, index: int) -> IShape:
        """Get the shape at the specified index. Supports negative indices."""
        shapes = self._load_shapes()
        # Python list indexing handles negative indices automatically
        try:
            return shapes[index]
        except IndexError:
            raise IndexError(f"Index {index} is out of range")


"""
Notes slide part handling for PPTX format.

Manages individual ppt/notesSlides/notesSlideN.xml parts.
"""

from __future__ import annotations
import lxml.etree as ET
from typing import Optional, TYPE_CHECKING

from .constants import NS, Elements, NAMESPACES
from ..opc import RelationshipsManager, ContentTypesManager
from ..opc.relationships import REL_TYPES
from ..opc.content_types import CONTENT_TYPES

if TYPE_CHECKING:
    from ..opc import OpcPackage

# Register namespaces for clean XML output
for prefix, uri in NAMESPACES.items():
    ET.register_namespace(prefix, uri)

# Notes slide placeholder types
_PH_TYPE_BODY = 'body'
_PH_TYPE_DT = 'dt'
_PH_TYPE_FTR = 'ftr'
_PH_TYPE_HDR = 'hdr'
_PH_TYPE_SLD_NUM = 'sldNum'
_PH_TYPE_SLD_IMG = 'sldImg'

# Text-bearing placeholder types
_TEXT_PH_TYPES = frozenset({_PH_TYPE_DT, _PH_TYPE_FTR, _PH_TYPE_HDR})


class NotesSlidePart:
    """
    Manages a notes slide XML part (ppt/notesSlides/notesSlideN.xml).

    Provides access to notes text and placeholder management.
    """

    def __init__(self, package: OpcPackage, part_name: str):
        """
        Initialize a notes slide part from an existing part in the package.

        Args:
            package: The OPC package containing the notes slide.
            part_name: The part path (e.g., 'ppt/notesSlides/notesSlide1.xml').
        """
        self._package = package
        self._part_name = part_name
        self._root: Optional[ET._Element] = None
        self._rels_manager = RelationshipsManager(package, part_name)
        self._load()

    def _load(self) -> None:
        """Load and parse the notes slide XML from the package."""
        content = self._package.get_part(self._part_name)
        if content:
            self._root = ET.fromstring(content)
        else:
            raise ValueError(f"Notes slide part not found: {self._part_name}")

    @property
    def part_name(self) -> str:
        """Get the part name of this notes slide."""
        return self._part_name

    @property
    def name(self) -> str:
        """Get the slide name from <p:cSld name='...'>."""
        csld = self._root.find(f".//{Elements.C_SLD}")
        if csld is not None:
            return csld.get('name', '')
        return ''

    @name.setter
    def name(self, value: str) -> None:
        """Set the slide name on <p:cSld name='...'>."""
        csld = self._root.find(f".//{Elements.C_SLD}")
        if csld is not None:
            csld.set('name', value)

    def _get_sp_tree(self) -> Optional[ET._Element]:
        """Get the spTree element from the notes slide."""
        return self._root.find(f".//{Elements.SP_TREE}")

    def _find_placeholder(self, ph_type: str) -> Optional[ET._Element]:
        """
        Find the first placeholder shape with the given type.

        Args:
            ph_type: The placeholder type string (e.g., 'body', 'ftr', 'hdr').

        Returns:
            The <p:sp> element or None if not found.
        """
        sp_tree = self._get_sp_tree()
        if sp_tree is None:
            return None

        for sp in sp_tree.findall(Elements.SP):
            nv_pr = sp.find(f"{Elements.NV_SP_PR}/{NS.P}nvPr")
            if nv_pr is None:
                continue
            ph = nv_pr.find(f"{NS.P}ph")
            if ph is None:
                continue
            if ph.get('type', '') == ph_type:
                return sp
        return None

    def get_notes_txbody(self) -> Optional[ET._Element]:
        """
        Get the txBody element of the notes body placeholder.

        Returns:
            The <a:txBody> / <p:txBody> element of the body placeholder, or None.
        """
        body_sp = self._find_placeholder(_PH_TYPE_BODY)
        if body_sp is not None:
            return body_sp.find(Elements.TX_BODY)
        return None

    def has_placeholder(self, ph_type: str) -> bool:
        """
        Check if a placeholder of the given type exists in the notes slide.

        Args:
            ph_type: The placeholder type string.

        Returns:
            True if the placeholder exists, False otherwise.
        """
        return self._find_placeholder(ph_type) is not None

    def remove_placeholder(self, ph_type: str) -> None:
        """
        Remove the placeholder shape of the given type.

        Args:
            ph_type: The placeholder type string to remove.
        """
        sp = self._find_placeholder(ph_type)
        if sp is not None:
            sp_tree = self._get_sp_tree()
            if sp_tree is not None:
                sp_tree.remove(sp)

    def add_placeholder(self, ph_type: str) -> None:
        """
        Add a minimal placeholder shape of the given type (if not already present).

        Args:
            ph_type: The placeholder type string to add.
        """
        if self.has_placeholder(ph_type):
            return

        sp_tree = self._get_sp_tree()
        if sp_tree is None:
            return

        # Find the next available shape ID
        max_id = 1
        for sp in sp_tree.findall(Elements.SP):
            nv_sp_pr = sp.find(Elements.NV_SP_PR)
            if nv_sp_pr is not None:
                c_nv_pr = nv_sp_pr.find(Elements.C_NV_PR)
                if c_nv_pr is not None:
                    try:
                        sp_id = int(c_nv_pr.get('id', '1'))
                        max_id = max(max_id, sp_id)
                    except ValueError:
                        pass

        shape_id = max_id + 1
        sp_elem = self._build_placeholder_shape(ph_type, shape_id)
        sp_tree.append(sp_elem)

    def _build_placeholder_shape(self, ph_type: str, shape_id: int) -> ET._Element:
        """
        Build a minimal placeholder shape element for notes slides.

        Args:
            ph_type: The placeholder type string.
            shape_id: The shape ID to assign.

        Returns:
            A new <p:sp> element.
        """
        sp = ET.Element(Elements.SP)

        nv_sp_pr = ET.SubElement(sp, Elements.NV_SP_PR)
        c_nv_pr = ET.SubElement(nv_sp_pr, Elements.C_NV_PR)
        c_nv_pr.set('id', str(shape_id))
        c_nv_pr.set('name', f'{ph_type} Placeholder {shape_id}')

        c_nv_sp_pr = ET.SubElement(nv_sp_pr, f"{NS.P}cNvSpPr")
        sp_locks = ET.SubElement(c_nv_sp_pr, f"{NS.A}spLocks")
        sp_locks.set('noGrp', '1')

        nv_pr = ET.SubElement(nv_sp_pr, f"{NS.P}nvPr")
        ph = ET.SubElement(nv_pr, f"{NS.P}ph")
        ph.set('type', ph_type)

        # Empty shape properties
        ET.SubElement(sp, Elements.SP_PR)

        # Add empty text body for text-bearing placeholders
        if ph_type in _TEXT_PH_TYPES:
            tx_body = ET.SubElement(sp, Elements.TX_BODY)
            ET.SubElement(tx_body, f"{NS.A}bodyPr")
            ET.SubElement(tx_body, f"{NS.A}lstStyle")
            a_p = ET.SubElement(tx_body, f"{NS.A}p")
            ET.SubElement(a_p, f"{NS.A}endParaRPr")

        return sp

    def set_placeholder_text(self, ph_type: str, text: str) -> None:
        """
        Set text content for a placeholder shape.

        Adds the placeholder if it does not exist.

        Args:
            ph_type: The placeholder type string.
            text: The text to set.
        """
        if not self.has_placeholder(ph_type):
            self.add_placeholder(ph_type)

        sp = self._find_placeholder(ph_type)
        if sp is None:
            return

        txbody = sp.find(Elements.TX_BODY)
        if txbody is None:
            txbody = ET.SubElement(sp, Elements.TX_BODY)
            ET.SubElement(txbody, f"{NS.A}bodyPr")
            ET.SubElement(txbody, f"{NS.A}lstStyle")

        # Remove existing paragraphs
        for p_elem in txbody.findall(f"{NS.A}p"):
            txbody.remove(p_elem)

        # Add new paragraph with the given text
        a_p = ET.SubElement(txbody, f"{NS.A}p")
        if text:
            a_r = ET.SubElement(a_p, f"{NS.A}r")
            a_t = ET.SubElement(a_r, f"{NS.A}t")
            a_t.text = text
        else:
            ET.SubElement(a_p, f"{NS.A}endParaRPr")

    def save(self) -> None:
        """Save the notes slide XML back to the package."""
        xml_bytes = ET.tostring(
            self._root,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8',
            standalone=True
        )
        self._package.set_part(self._part_name, xml_bytes)
        self._rels_manager.save()

    def _resolve_target(self, target: str) -> str:
        """Resolve a relative target path to an absolute part name."""
        if target.startswith('/'):
            return target.lstrip('/')
        base_dir = self._part_name.rsplit('/', 1)[0] if '/' in self._part_name else ''
        parts = (base_dir + '/' + target).split('/')
        resolved = []
        for part in parts:
            if part == '..':
                if resolved:
                    resolved.pop()
            elif part and part != '.':
                resolved.append(part)
        return '/'.join(resolved)

    @staticmethod
    def create_empty(package: OpcPackage, slide_part_name: str) -> 'NotesSlidePart':
        """
        Create a new empty notes slide in the package for a given slide.

        Args:
            package: The OPC package.
            slide_part_name: The part name of the owning slide.

        Returns:
            The newly created NotesSlidePart.
        """
        # Find the next available notes slide number
        next_num = 1
        while True:
            candidate = f"ppt/notesSlides/notesSlide{next_num}.xml"
            if not package.has_part(candidate):
                part_name = candidate
                break
            next_num += 1

        # Build and store the notes slide XML
        notes_xml = NotesSlidePart._build_notes_xml()
        package.set_part(part_name, notes_xml)

        # Create the notes slide's own relationships
        rels_manager = RelationshipsManager(package, part_name)

        # Relationship: notes slide → parent slide
        slide_relative = NotesSlidePart._compute_relative_target(part_name, slide_part_name)
        rels_manager.add_relationship(REL_TYPES['slide'], slide_relative)

        # Relationship: notes slide → notes master (if present)
        notes_master_part_name = NotesSlidePart._find_notes_master(package)
        if notes_master_part_name:
            master_relative = NotesSlidePart._compute_relative_target(
                part_name, notes_master_part_name
            )
            rels_manager.add_relationship(REL_TYPES['notes_master'], master_relative)

        rels_manager.save()

        # Register content type
        ct_manager = ContentTypesManager(package)
        ct_manager.add_override(part_name, CONTENT_TYPES['notes_slide'])
        ct_manager.save()

        return NotesSlidePart(package, part_name)

    @staticmethod
    def _find_notes_master(package: OpcPackage) -> Optional[str]:
        """
        Find the notes master part name in the package.

        Returns:
            The part name of the notes master, or None if not found.
        """
        for part in package.get_part_names():
            if part.startswith('ppt/notesMasters/') and part.endswith('.xml'):
                return part
        return None

    @staticmethod
    def _compute_relative_target(from_part: str, to_part: str) -> str:
        """Compute a relative path from one part to another."""
        from_dir = from_part.rsplit('/', 1)[0] if '/' in from_part else ''
        to_dir = to_part.rsplit('/', 1)[0] if '/' in to_part else ''
        to_file = to_part.rsplit('/', 1)[-1]

        if from_dir == to_dir:
            return to_file

        from_parts = from_dir.split('/') if from_dir else []
        to_parts = to_dir.split('/') if to_dir else []

        # Find common prefix length
        common_len = 0
        for i in range(min(len(from_parts), len(to_parts))):
            if from_parts[i] == to_parts[i]:
                common_len = i + 1
            else:
                break

        up_count = len(from_parts) - common_len
        down_path = '/'.join(to_parts[common_len:])

        result = '../' * up_count
        if down_path:
            result += down_path + '/'
        result += to_file

        return result

    @staticmethod
    def _build_notes_xml() -> bytes:
        """
        Build a minimal notes slide XML with a slide image and body placeholder.

        Returns:
            UTF-8 encoded XML bytes.
        """
        nsmap = {
            'a': NAMESPACES['a'],
            'r': NAMESPACES['r'],
            'p': NAMESPACES['p'],
        }
        notes = ET.Element(f"{NS.P}notes", nsmap=nsmap)

        # <p:cSld>
        c_sld = ET.SubElement(notes, Elements.C_SLD)
        sp_tree = ET.SubElement(c_sld, Elements.SP_TREE)

        # Group shape header (required)
        nv_grp_sp_pr = ET.SubElement(sp_tree, f"{NS.P}nvGrpSpPr")
        c_nv_pr_grp = ET.SubElement(nv_grp_sp_pr, Elements.C_NV_PR)
        c_nv_pr_grp.set('id', '1')
        c_nv_pr_grp.set('name', '')
        ET.SubElement(nv_grp_sp_pr, f"{NS.P}cNvGrpSpPr")
        ET.SubElement(nv_grp_sp_pr, f"{NS.P}nvPr")

        grp_sp_pr = ET.SubElement(sp_tree, f"{NS.P}grpSpPr")
        xfrm = ET.SubElement(grp_sp_pr, f"{NS.A}xfrm")
        off = ET.SubElement(xfrm, f"{NS.A}off")
        off.set('x', '0')
        off.set('y', '0')
        ext = ET.SubElement(xfrm, f"{NS.A}ext")
        ext.set('cx', '0')
        ext.set('cy', '0')
        ch_off = ET.SubElement(xfrm, f"{NS.A}chOff")
        ch_off.set('x', '0')
        ch_off.set('y', '0')
        ch_ext = ET.SubElement(xfrm, f"{NS.A}chExt")
        ch_ext.set('cx', '0')
        ch_ext.set('cy', '0')

        # Slide image placeholder (type="sldImg")
        sp1 = ET.SubElement(sp_tree, Elements.SP)
        nv_sp_pr1 = ET.SubElement(sp1, Elements.NV_SP_PR)
        c_nv_pr1 = ET.SubElement(nv_sp_pr1, Elements.C_NV_PR)
        c_nv_pr1.set('id', '2')
        c_nv_pr1.set('name', 'Slide Image Placeholder 1')
        c_nv_sp_pr1 = ET.SubElement(nv_sp_pr1, f"{NS.P}cNvSpPr")
        sp_locks1 = ET.SubElement(c_nv_sp_pr1, f"{NS.A}spLocks")
        sp_locks1.set('noGrp', '1')
        nv_pr1 = ET.SubElement(nv_sp_pr1, f"{NS.P}nvPr")
        ph1 = ET.SubElement(nv_pr1, f"{NS.P}ph")
        ph1.set('type', 'sldImg')
        ET.SubElement(sp1, Elements.SP_PR)

        # Notes body placeholder (type="body", idx="1")
        sp2 = ET.SubElement(sp_tree, Elements.SP)
        nv_sp_pr2 = ET.SubElement(sp2, Elements.NV_SP_PR)
        c_nv_pr2 = ET.SubElement(nv_sp_pr2, Elements.C_NV_PR)
        c_nv_pr2.set('id', '3')
        c_nv_pr2.set('name', 'Notes Placeholder 2')
        c_nv_sp_pr2 = ET.SubElement(nv_sp_pr2, f"{NS.P}cNvSpPr")
        sp_locks2 = ET.SubElement(c_nv_sp_pr2, f"{NS.A}spLocks")
        sp_locks2.set('noGrp', '1')
        nv_pr2 = ET.SubElement(nv_sp_pr2, f"{NS.P}nvPr")
        ph2 = ET.SubElement(nv_pr2, f"{NS.P}ph")
        ph2.set('type', 'body')
        ph2.set('idx', '1')
        ET.SubElement(sp2, Elements.SP_PR)
        tx_body = ET.SubElement(sp2, Elements.TX_BODY)
        ET.SubElement(tx_body, f"{NS.A}bodyPr")
        ET.SubElement(tx_body, f"{NS.A}lstStyle")
        a_p = ET.SubElement(tx_body, f"{NS.A}p")
        ET.SubElement(a_p, f"{NS.A}endParaRPr")

        # Color map override
        clr_map_ovr = ET.SubElement(notes, f"{NS.P}clrMapOvr")
        ET.SubElement(clr_map_ovr, f"{NS.A}masterClrMapping")

        return ET.tostring(
            notes,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8',
            standalone=True
        )

    @staticmethod
    def delete(package: OpcPackage, part_name: str) -> None:
        """
        Delete a notes slide and its associated files from the package.

        Args:
            package: The OPC package.
            part_name: The notes slide part name to delete.
        """
        package.delete_part(part_name)

        rels_part_name = RelationshipsManager._get_rels_part_name(part_name)
        package.delete_part(rels_part_name)

        ct_manager = ContentTypesManager(package)
        ct_manager.remove_override(part_name)
        ct_manager.save()

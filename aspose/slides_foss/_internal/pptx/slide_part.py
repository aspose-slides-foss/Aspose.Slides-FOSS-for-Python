"""
Slide part handling for PPTX format.

Manages individual ppt/slides/slideN.xml parts.
"""

from __future__ import annotations
import copy
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

# System placeholder types that should NOT be copied to new slides.
# These are rendered by the master slide / presentation engine.
_SYSTEM_PLACEHOLDER_TYPES = frozenset({'dt', 'ftr', 'sldNum', 'hdr'})


class SlidePart:
    """
    Manages an individual slide XML part (ppt/slides/slideN.xml).

    Provides access to slide properties and relationships.
    """

    def __init__(self, package: OpcPackage, part_name: str):
        """
        Initialize a slide part from an existing part in the package.

        Args:
            package: The OPC package containing the slide.
            part_name: The part path (e.g., 'ppt/slides/slide1.xml').
        """
        self._package = package
        self._part_name = part_name
        self._root: Optional[ET._Element] = None
        self._rels_manager = RelationshipsManager(package, part_name)
        self._load()

    def _load(self) -> None:
        """Load and parse the slide XML from the package."""
        content = self._package.get_part(self._part_name)
        if content:
            self._root = ET.fromstring(content)
        else:
            raise ValueError(f"Slide part not found: {self._part_name}")

    @property
    def part_name(self) -> str:
        """Get the part name of this slide."""
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

    @property
    def hidden(self) -> bool:
        """Check if slide is hidden (show='0' attribute on root)."""
        show = self._root.get('show')
        return show == '0'

    @hidden.setter
    def hidden(self, value: bool) -> None:
        """Set slide hidden state."""
        if value:
            self._root.set('show', '0')
        else:
            if 'show' in self._root.attrib:
                del self._root.attrib['show']

    @property
    def layout_rel_id(self) -> Optional[str]:
        """Get the relationship ID for the layout slide."""
        rels = self._rels_manager.get_relationships_by_type(REL_TYPES['slide_layout'])
        if rels:
            return rels[0].id
        return None

    @property
    def layout_part_name(self) -> Optional[str]:
        """Resolve the layout slide part name from the relationship."""
        rels = self._rels_manager.get_relationships_by_type(REL_TYPES['slide_layout'])
        if rels:
            target = rels[0].target
            return self._resolve_target(target)
        return None

    def _resolve_target(self, target: str) -> str:
        """Resolve a relative target path to an absolute part name."""
        if target.startswith('/'):
            return target.lstrip('/')
        # Resolve relative to the directory of this part
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

    def save(self) -> None:
        """Save the slide XML back to the package."""
        xml_bytes = ET.tostring(
            self._root,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8',
            standalone=True
        )
        self._package.set_part(self._part_name, xml_bytes)
        self._rels_manager.save()

    @staticmethod
    def create_empty(package: OpcPackage, part_name: str, layout_part_name: str) -> SlidePart:
        """
        Create a new empty slide in the package.

        The slide inherits content placeholder shapes from the layout
        (title, subtitle, content, etc.) but not system placeholders
        (date, footer, slide number).

        Args:
            package: The OPC package.
            part_name: The part name for the new slide (e.g., 'ppt/slides/slide2.xml').
            layout_part_name: The part name of the layout to reference.

        Returns:
            The created SlidePart.
        """
        # Build placeholder shapes from the layout
        placeholder_shapes = SlidePart._extract_placeholder_shapes(package, layout_part_name)

        # Create the slide XML with placeholders
        slide_xml = SlidePart._build_slide_xml(placeholder_shapes)
        package.set_part(part_name, slide_xml)

        # Create relationships for the slide
        rels_manager = RelationshipsManager(package, part_name)

        # Compute relative target from slide to layout
        slide_dir = part_name.rsplit('/', 1)[0] if '/' in part_name else ''
        layout_dir = layout_part_name.rsplit('/', 1)[0] if '/' in layout_part_name else ''
        layout_file = layout_part_name.rsplit('/', 1)[-1]

        if slide_dir == layout_dir:
            relative_target = layout_file
        else:
            relative_target = f"../{layout_dir.split('/')[-1]}/{layout_file}"

        rels_manager.add_relationship(REL_TYPES['slide_layout'], relative_target)
        rels_manager.save()

        # Add content type override
        ct_manager = ContentTypesManager(package)
        ct_manager.add_override(part_name, CONTENT_TYPES['slide'])
        ct_manager.save()

        return SlidePart(package, part_name)

    @staticmethod
    def _extract_placeholder_shapes(package: OpcPackage, layout_part_name: str) -> list[ET._Element]:
        """
        Extract content placeholder shapes from a layout slide.

        Reads the layout XML, finds all <p:sp> elements that contain a
        <p:ph> placeholder marker, and returns copies of those that are
        content placeholders (excluding system ones like date/footer/sldNum).

        Each returned shape has:
        - Its <p:nvSpPr> preserved (placeholder type/idx reference)
        - An empty <p:spPr/> (position inherited from layout at runtime)
        - An empty text body (no template text)
        - A new sequential shape ID starting from 2

        Args:
            package: The OPC package.
            layout_part_name: Path to the layout XML in the package.

        Returns:
            List of lxml Element objects (<p:sp>) ready to insert.
        """
        layout_content = package.get_part(layout_part_name)
        if not layout_content:
            return []

        layout_root = ET.fromstring(layout_content)
        sp_tree = layout_root.find(f".//{Elements.SP_TREE}")
        if sp_tree is None:
            return []

        result = []
        shape_id = 2  # id=1 is reserved for the group shape

        for sp in sp_tree.findall(Elements.SP):
            nv_pr = sp.find(f"{Elements.NV_SP_PR}/{NS.P}nvPr")
            if nv_pr is None:
                continue
            ph = nv_pr.find(f"{NS.P}ph")
            if ph is None:
                continue

            ph_type = ph.get('type', '')
            if ph_type in _SYSTEM_PLACEHOLDER_TYPES:
                continue

            # Build a clean copy of this placeholder for the new slide
            new_sp = SlidePart._build_placeholder_shape(sp, shape_id)
            result.append(new_sp)
            shape_id += 1

        return result

    @staticmethod
    def _build_placeholder_shape(layout_sp: ET._Element, shape_id: int) -> ET._Element:
        """
        Build a slide placeholder shape from a layout placeholder shape.

        Preserves the nvSpPr (with placeholder marker) but clears the
        shape properties and text body so the slide inherits from layout.

        Args:
            layout_sp: The <p:sp> element from the layout.
            shape_id: The new shape ID to assign.

        Returns:
            A new <p:sp> element for the slide.
        """
        # Deep-copy the entire nvSpPr to keep placeholder info, locks, etc.
        nv_sp_pr = layout_sp.find(Elements.NV_SP_PR)
        new_nv_sp_pr = copy.deepcopy(nv_sp_pr)

        # Update the shape ID
        c_nv_pr = new_nv_sp_pr.find(Elements.C_NV_PR)
        if c_nv_pr is not None:
            c_nv_pr.set('id', str(shape_id))

        # Build the new <p:sp> element
        new_sp = ET.Element(Elements.SP)
        new_sp.append(new_nv_sp_pr)

        # Empty spPr — position/size inherited from layout
        ET.SubElement(new_sp, Elements.SP_PR)

        # Empty text body
        tx_body = ET.SubElement(new_sp, Elements.TX_BODY)
        ET.SubElement(tx_body, f"{NS.A}bodyPr")
        ET.SubElement(tx_body, f"{NS.A}lstStyle")
        a_p = ET.SubElement(tx_body, f"{NS.A}p")
        ET.SubElement(a_p, f"{NS.A}endParaRPr")

        return new_sp

    @staticmethod
    def _build_slide_xml(placeholder_shapes: list[ET._Element]) -> bytes:
        """
        Build the complete slide XML with the given placeholder shapes.

        Args:
            placeholder_shapes: List of <p:sp> elements to include.

        Returns:
            UTF-8 encoded XML bytes.
        """
        # Build the root <p:sld> element with proper namespaces
        nsmap = {
            'a': NAMESPACES['a'],
            'r': NAMESPACES['r'],
            'p': NAMESPACES['p'],
        }
        sld = ET.Element(f"{NS.P}sld", nsmap=nsmap)

        # <p:cSld>
        c_sld = ET.SubElement(sld, Elements.C_SLD)

        # <p:spTree>
        sp_tree = ET.SubElement(c_sld, Elements.SP_TREE)

        # Group shape properties (always required, id=1)
        nv_grp_sp_pr = ET.SubElement(sp_tree, f"{NS.P}nvGrpSpPr")
        c_nv_pr = ET.SubElement(nv_grp_sp_pr, Elements.C_NV_PR)
        c_nv_pr.set('id', '1')
        c_nv_pr.set('name', '')
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

        # Append placeholder shapes
        for sp in placeholder_shapes:
            sp_tree.append(sp)

        # <p:clrMapOvr>
        clr_map_ovr = ET.SubElement(sld, f"{NS.P}clrMapOvr")
        ET.SubElement(clr_map_ovr, f"{NS.A}masterClrMapping")

        return ET.tostring(
            sld,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8',
            standalone=True
        )

    @staticmethod
    def delete(package: OpcPackage, part_name: str) -> None:
        """
        Delete a slide and its associated files from the package.

        Args:
            package: The OPC package.
            part_name: The slide part name to delete.
        """
        # Delete the slide XML
        package.delete_part(part_name)

        # Delete the slide's .rels file
        rels_part_name = RelationshipsManager._get_rels_part_name(part_name)
        package.delete_part(rels_part_name)

        # Remove content type override
        ct_manager = ContentTypesManager(package)
        ct_manager.remove_override(part_name)
        ct_manager.save()

    @staticmethod
    def clone_from(
        source_package: OpcPackage,
        source_part_name: str,
        dest_package: OpcPackage,
        dest_part_name: str,
        dest_layout_part_name: Optional[str] = None
    ) -> 'SlidePart':
        """
        Clone a slide from a source package to a destination package.

        This performs a deep copy of the slide and all its related parts
        (charts, images, embedded objects, etc.), updating relationship IDs
        as needed.

        Args:
            source_package: The source OPC package.
            source_part_name: The source slide part name.
            dest_package: The destination OPC package (can be the same as source).
            dest_part_name: The destination slide part name.
            dest_layout_part_name: Optional layout to use. If None, uses the source layout
                                   (must exist in dest_package).

        Returns:
            The cloned SlidePart.
        """
        # Load source slide XML
        source_content = source_package.get_part(source_part_name)
        if not source_content:
            raise ValueError(f"Source slide not found: {source_part_name}")

        source_root = ET.fromstring(source_content)

        # Deep copy the slide XML
        dest_root = copy.deepcopy(source_root)

        # Load source relationships
        source_rels = RelationshipsManager(source_package, source_part_name)

        # Create destination relationships manager
        dest_rels = RelationshipsManager(dest_package, dest_part_name)

        # Track old rId -> new rId mapping for updating XML references
        rid_mapping: dict[str, str] = {}

        # Process each relationship from source
        same_package = source_package is dest_package
        for rel in source_rels.get_all_relationships():
            if rel.type == REL_TYPES['slide_layout']:
                # Handle layout relationship specially
                if dest_layout_part_name:
                    layout_part = dest_layout_part_name
                else:
                    # Resolve the source layout and use it in destination
                    layout_part = SlidePart._resolve_target_static(
                        source_part_name, rel.target
                    )

                # Compute relative target from dest slide to layout
                relative_target = SlidePart._compute_relative_target(
                    dest_part_name, layout_part
                )
                new_rid = dest_rels.add_relationship(rel.type, relative_target)
                rid_mapping[rel.id] = new_rid

            elif rel.target_mode == 'External':
                # External links (hyperlinks, etc.) - just copy the relationship
                new_rid = dest_rels.add_relationship(
                    rel.type, rel.target, target_mode='External'
                )
                rid_mapping[rel.id] = new_rid

            else:
                # Internal parts (charts, images, etc.) - need to copy the part
                source_target_path = SlidePart._resolve_target_static(
                    source_part_name, rel.target
                )

                if same_package:
                    # Same package - can reuse images/media, but must copy charts
                    if SlidePart._is_shared_resource(rel.type):
                        # Reuse the existing resource
                        relative_target = SlidePart._compute_relative_target(
                            dest_part_name, source_target_path
                        )
                        new_rid = dest_rels.add_relationship(rel.type, relative_target)
                    else:
                        # Clone the part (charts, notes, etc.)
                        new_target_path = SlidePart._clone_related_part(
                            source_package, source_target_path,
                            dest_package, dest_part_name, rel.type
                        )
                        relative_target = SlidePart._compute_relative_target(
                            dest_part_name, new_target_path
                        )
                        new_rid = dest_rels.add_relationship(rel.type, relative_target)
                else:
                    # Different packages - must copy everything
                    new_target_path = SlidePart._clone_related_part(
                        source_package, source_target_path,
                        dest_package, dest_part_name, rel.type
                    )
                    relative_target = SlidePart._compute_relative_target(
                        dest_part_name, new_target_path
                    )
                    new_rid = dest_rels.add_relationship(rel.type, relative_target)

                rid_mapping[rel.id] = new_rid

        # Update all r:id and r:embed references in the cloned XML
        SlidePart._update_rid_references(dest_root, rid_mapping)

        # Save the cloned slide XML
        xml_bytes = ET.tostring(
            dest_root,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8',
            standalone=True
        )
        dest_package.set_part(dest_part_name, xml_bytes)

        # Save relationships
        dest_rels.save()

        # Add content type override
        ct_manager = ContentTypesManager(dest_package)
        ct_manager.add_override(dest_part_name, CONTENT_TYPES['slide'])
        ct_manager.save()

        return SlidePart(dest_package, dest_part_name)

    @staticmethod
    def _resolve_target_static(source_part: str, target: str) -> str:
        """Resolve a relative target path to an absolute part name."""
        if target.startswith('/'):
            return target.lstrip('/')
        base_dir = source_part.rsplit('/', 1)[0] if '/' in source_part else ''
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
    def _compute_relative_target(from_part: str, to_part: str) -> str:
        """Compute a relative path from one part to another."""
        from_dir = from_part.rsplit('/', 1)[0] if '/' in from_part else ''
        to_dir = to_part.rsplit('/', 1)[0] if '/' in to_part else ''
        to_file = to_part.rsplit('/', 1)[-1]

        if from_dir == to_dir:
            return to_file

        # Count how many levels up we need to go
        from_parts = from_dir.split('/') if from_dir else []
        to_parts = to_dir.split('/') if to_dir else []

        # Find common prefix
        common_len = 0
        for i in range(min(len(from_parts), len(to_parts))):
            if from_parts[i] == to_parts[i]:
                common_len = i + 1
            else:
                break

        # Build relative path
        up_count = len(from_parts) - common_len
        down_path = '/'.join(to_parts[common_len:])

        result = '../' * up_count
        if down_path:
            result += down_path + '/'
        result += to_file

        return result

    @staticmethod
    def _is_shared_resource(rel_type: str) -> bool:
        """Check if a relationship type refers to a shared resource (can be reused)."""
        # Images and media files can be shared across slides
        shared_types = {
            REL_TYPES.get('image'),
            'http://schemas.openxmlformats.org/officeDocument/2006/relationships/audio',
            'http://schemas.openxmlformats.org/officeDocument/2006/relationships/video',
        }
        return rel_type in shared_types

    @staticmethod
    def _clone_related_part(
        source_package: OpcPackage,
        source_path: str,
        dest_package: OpcPackage,
        dest_slide_part: str,
        rel_type: str
    ) -> str:
        """
        Clone a related part (chart, image, etc.) to the destination package.

        Returns the new part path in the destination package.
        """
        import re

        # Determine the destination path based on part type
        source_content = source_package.get_part(source_path)
        if source_content is None:
            # Part doesn't exist, skip
            return source_path

        # Get the directory and filename from source
        if '/' in source_path:
            source_dir, source_file = source_path.rsplit('/', 1)
        else:
            source_dir, source_file = '', source_path

        # Determine destination directory based on relationship type
        is_xml_part = False
        if 'chart' in rel_type.lower():
            dest_dir = 'ppt/charts'
            ext = '.xml'
            is_xml_part = True
        elif 'image' in rel_type.lower():
            dest_dir = 'ppt/media'
            ext = '.' + source_file.rsplit('.', 1)[-1] if '.' in source_file else ''
        elif 'notesSlide' in rel_type:
            dest_dir = 'ppt/notesSlides'
            ext = '.xml'
            is_xml_part = True
        else:
            # Keep in same directory structure
            dest_dir = source_dir
            ext = '.' + source_file.rsplit('.', 1)[-1] if '.' in source_file else ''
            # Check if it's an XML file
            is_xml_part = ext == '.xml'

        # Find next available number for this type of part
        # First, strip the extension from the source filename
        if '.' in source_file:
            source_name_no_ext = source_file.rsplit('.', 1)[0]
        else:
            source_name_no_ext = source_file

        # Remove trailing numbers to get the base name
        base_name = re.sub(r'\d+$', '', source_name_no_ext)
        if not base_name:
            base_name = 'part'

        next_num = 1
        while True:
            candidate = f"{dest_dir}/{base_name}{next_num}{ext}"
            if not dest_package.has_part(candidate):
                dest_path = candidate
                break
            next_num += 1

        # Copy content type if needed
        source_ct_manager = ContentTypesManager(source_package)
        source_ct = source_ct_manager.get_content_type(source_path)
        if source_ct:
            dest_ct_manager = ContentTypesManager(dest_package)
            dest_ct_manager.add_override(dest_path, source_ct)
            dest_ct_manager.save()

        # If the part has its own relationships (e.g., charts), clone those too
        source_part_rels = RelationshipsManager(source_package, source_path)
        all_rels = source_part_rels.get_all_relationships()

        # Track rId mapping for updating XML references
        rid_mapping: dict[str, str] = {}

        if all_rels:
            dest_part_rels = RelationshipsManager(dest_package, dest_path)
            for sub_rel in all_rels:
                if sub_rel.target_mode == 'External':
                    new_rid = dest_part_rels.add_relationship(
                        sub_rel.type, sub_rel.target, target_mode='External'
                    )
                else:
                    # Recursively clone sub-parts
                    sub_source_path = SlidePart._resolve_target_static(
                        source_path, sub_rel.target
                    )
                    sub_dest_path = SlidePart._clone_related_part(
                        source_package, sub_source_path,
                        dest_package, dest_path, sub_rel.type
                    )
                    sub_relative = SlidePart._compute_relative_target(
                        dest_path, sub_dest_path
                    )
                    new_rid = dest_part_rels.add_relationship(sub_rel.type, sub_relative)
                rid_mapping[sub_rel.id] = new_rid
            dest_part_rels.save()

        # If it's an XML part and we have rId mappings, update the XML content
        if is_xml_part and rid_mapping:
            try:
                source_root = ET.fromstring(source_content)
                dest_root = copy.deepcopy(source_root)
                SlidePart._update_rid_references(dest_root, rid_mapping)
                dest_content = ET.tostring(
                    dest_root,
                    pretty_print=True,
                    xml_declaration=True,
                    encoding='UTF-8',
                    standalone=True
                )
                dest_package.set_part(dest_path, dest_content)
            except ET.XMLSyntaxError:
                # Not valid XML, just copy as-is
                dest_package.set_part(dest_path, source_content)
        else:
            # Copy the content as-is
            dest_package.set_part(dest_path, source_content)

        return dest_path

    @staticmethod
    def _update_rid_references(root: ET._Element, rid_mapping: dict[str, str]) -> None:
        """Update all r:id and r:embed attribute references in an XML tree."""
        r_ns = NAMESPACES['r']
        r_id_attr = f"{{{r_ns}}}id"
        r_embed_attr = f"{{{r_ns}}}embed"
        r_link_attr = f"{{{r_ns}}}link"

        for elem in root.iter():
            # Check r:id
            if r_id_attr in elem.attrib:
                old_id = elem.attrib[r_id_attr]
                if old_id in rid_mapping:
                    elem.attrib[r_id_attr] = rid_mapping[old_id]

            # Check r:embed
            if r_embed_attr in elem.attrib:
                old_id = elem.attrib[r_embed_attr]
                if old_id in rid_mapping:
                    elem.attrib[r_embed_attr] = rid_mapping[old_id]

            # Check r:link
            if r_link_attr in elem.attrib:
                old_id = elem.attrib[r_link_attr]
                if old_id in rid_mapping:
                    elem.attrib[r_link_attr] = rid_mapping[old_id]

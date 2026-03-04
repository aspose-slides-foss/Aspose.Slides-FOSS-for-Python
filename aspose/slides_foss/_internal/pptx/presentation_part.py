"""
Presentation part handling for PPTX format.

Manages the ppt/presentation.xml part which is the main entry point
for a PowerPoint presentation.
"""

from __future__ import annotations
import lxml.etree as ET
from typing import Optional, TYPE_CHECKING

from .constants import NS, Elements, Attributes, NAMESPACES

if TYPE_CHECKING:
    from ..opc import OpcPackage

# Register namespaces for clean XML output
for prefix, uri in NAMESPACES.items():
    ET.register_namespace(prefix, uri)


class SlideReference:
    """Reference to a slide in the presentation."""

    def __init__(self, slide_id: int, rel_id: str):
        """
        Initialize a slide reference.

        Args:
            slide_id: The unique slide ID (id attribute).
            rel_id: The relationship ID (r:id attribute).
        """
        self.slide_id = slide_id
        self.rel_id = rel_id


class MasterReference:
    """Reference to a master slide in the presentation."""

    def __init__(self, master_id: int, rel_id: str):
        """
        Initialize a master slide reference.

        Args:
            master_id: The unique master slide ID (id attribute).
            rel_id: The relationship ID (r:id attribute).
        """
        self.master_id = master_id
        self.rel_id = rel_id


class PresentationPart:
    """
    Manages the ppt/presentation.xml part.

    This class provides methods to:
    - Parse presentation structure (slides, masters, sizes)
    - Add/remove slide references
    - Get/set presentation properties
    - Serialize back to XML
    """

    PART_NAME = 'ppt/presentation.xml'

    def __init__(self, package: OpcPackage):
        """
        Initialize the presentation part manager.

        Args:
            package: The OPC package containing the presentation.
        """
        self._package = package
        self._root: Optional[ET._Element] = None
        self._slide_refs: list[SlideReference] = []
        self._master_refs: list[MasterReference] = []
        self._load()

    def _load(self) -> None:
        """Load and parse the presentation.xml from the package."""
        content = self._package.get_part(self.PART_NAME)
        if content:
            self._root = ET.fromstring(content)
            self._parse_slides()
            self._parse_masters()
        else:
            raise ValueError(f"{self.PART_NAME} not found in package")

    def _parse_slides(self) -> None:
        """Parse slide references from the presentation XML."""
        self._slide_refs.clear()

        sld_id_lst = self._root.find(f".//{Elements.SLD_ID_LST}")
        if sld_id_lst is not None:
            for sld_id_elem in sld_id_lst.findall(Elements.SLD_ID):
                slide_id = int(sld_id_elem.get(Attributes.ID, '0'))
                rel_id = sld_id_elem.get(Attributes.R_ID, '')
                self._slide_refs.append(SlideReference(slide_id, rel_id))

    def _parse_masters(self) -> None:
        """Parse master slide references from the presentation XML."""
        self._master_refs.clear()

        sld_master_id_lst = self._root.find(f".//{Elements.SLD_MASTER_ID_LST}")
        if sld_master_id_lst is not None:
            for sld_master_id_elem in sld_master_id_lst.findall(Elements.SLD_MASTER_ID):
                master_id = int(sld_master_id_elem.get(Attributes.ID, '0'))
                rel_id = sld_master_id_elem.get(Attributes.R_ID, '')
                self._master_refs.append(MasterReference(master_id, rel_id))

    @property
    def master_references(self) -> list[MasterReference]:
        """Get the list of master slide references."""
        return self._master_refs.copy()

    @property
    def element_tree(self) -> Optional[ET._Element]:
        """Get the root element of the presentation XML."""
        return self._root

    @property
    def slide_references(self) -> list[SlideReference]:
        """Get the list of slide references in order."""
        return self._slide_refs.copy()

    @property
    def slide_count(self) -> int:
        """Get the number of slides."""
        return len(self._slide_refs)

    def get_slide_ref_by_id(self, slide_id: int) -> Optional[SlideReference]:
        """
        Get a slide reference by its slide ID.

        Args:
            slide_id: The unique slide ID.

        Returns:
            SlideReference or None if not found.
        """
        for ref in self._slide_refs:
            if ref.slide_id == slide_id:
                return ref
        return None

    def get_slide_ref_by_rel_id(self, rel_id: str) -> Optional[SlideReference]:
        """
        Get a slide reference by its relationship ID.

        Args:
            rel_id: The relationship ID (e.g., 'rId2').

        Returns:
            SlideReference or None if not found.
        """
        for ref in self._slide_refs:
            if ref.rel_id == rel_id:
                return ref
        return None

    def _get_next_slide_id(self) -> int:
        """Generate the next available slide ID."""
        if not self._slide_refs:
            return 256  # PPTX convention: slide IDs start at 256
        return max(ref.slide_id for ref in self._slide_refs) + 1

    def _get_next_master_id(self) -> int:
        """Generate the next available master/layout slide ID.

        In PPTX, master IDs (sldMasterIdLst) and layout IDs (sldLayoutIdLst)
        share the same ID space and must all be unique. This method scans both
        to find the next available ID.
        """
        max_id = 2147483647  # One below the PPTX convention start

        # Check existing master IDs
        for ref in self._master_refs:
            if ref.master_id > max_id:
                max_id = ref.master_id

        # Check existing layout IDs across all master slides in the package
        ns_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'
        for part_name in self._package.get_part_names():
            if part_name.startswith('ppt/slideMasters/') and part_name.endswith('.xml'):
                content = self._package.get_part(part_name)
                if content:
                    import lxml.etree as _ET
                    root = _ET.fromstring(content)
                    for elem in root.iter(f'{{{ns_p}}}sldLayoutId'):
                        layout_id = int(elem.get('id', '0'))
                        if layout_id > max_id:
                            max_id = layout_id

        return max_id + 1

    def add_master_reference(self, rel_id: str, master_id: Optional[int] = None) -> MasterReference:
        """
        Add a new master slide reference to the presentation.

        Args:
            rel_id: The relationship ID for the master slide.
            master_id: Optional specific master ID. If None, auto-generated.

        Returns:
            The created MasterReference.
        """
        if master_id is None:
            master_id = self._get_next_master_id()

        ref = MasterReference(master_id, rel_id)
        self._master_refs.append(ref)

        # Add to XML
        sld_master_id_lst = self._root.find(f".//{Elements.SLD_MASTER_ID_LST}")
        if sld_master_id_lst is None:
            # Create sldMasterIdLst if it doesn't exist (insert before sldIdLst)
            sld_id_lst = self._root.find(f".//{Elements.SLD_ID_LST}")
            if sld_id_lst is not None:
                idx = list(self._root).index(sld_id_lst)
                sld_master_id_lst = ET.Element(Elements.SLD_MASTER_ID_LST)
                self._root.insert(idx, sld_master_id_lst)
            else:
                sld_master_id_lst = ET.SubElement(self._root, Elements.SLD_MASTER_ID_LST)

        sld_master_id_elem = ET.Element(Elements.SLD_MASTER_ID)
        sld_master_id_elem.set(Attributes.ID, str(master_id))
        sld_master_id_elem.set(Attributes.R_ID, rel_id)
        sld_master_id_lst.append(sld_master_id_elem)

        return ref

    def add_slide_reference(self, rel_id: str, slide_id: Optional[int] = None, index: int = -1) -> SlideReference:
        """
        Add a new slide reference to the presentation.

        Args:
            rel_id: The relationship ID for the slide.
            slide_id: Optional specific slide ID. If None, auto-generated.
            index: Position to insert at. -1 means append at end.

        Returns:
            The created SlideReference.
        """
        if slide_id is None:
            slide_id = self._get_next_slide_id()

        ref = SlideReference(slide_id, rel_id)

        # Add to internal list
        if index < 0 or index >= len(self._slide_refs):
            self._slide_refs.append(ref)
        else:
            self._slide_refs.insert(index, ref)

        # Add to XML
        sld_id_lst = self._root.find(f".//{Elements.SLD_ID_LST}")
        if sld_id_lst is None:
            # Create sldIdLst if it doesn't exist
            sld_id_lst = ET.SubElement(self._root, Elements.SLD_ID_LST)

        sld_id_elem = ET.Element(Elements.SLD_ID)
        sld_id_elem.set(Attributes.ID, str(slide_id))
        sld_id_elem.set(Attributes.R_ID, rel_id)

        if index < 0 or index >= len(sld_id_lst):
            sld_id_lst.append(sld_id_elem)
        else:
            sld_id_lst.insert(index, sld_id_elem)

        return ref

    def remove_slide_reference(self, slide_id: int) -> bool:
        """
        Remove a slide reference by its slide ID.

        Args:
            slide_id: The unique slide ID to remove.

        Returns:
            True if removed, False if not found.
        """
        # Find and remove from internal list
        ref_to_remove = None
        for i, ref in enumerate(self._slide_refs):
            if ref.slide_id == slide_id:
                ref_to_remove = ref
                self._slide_refs.pop(i)
                break

        if ref_to_remove is None:
            return False

        # Remove from XML
        sld_id_lst = self._root.find(f".//{Elements.SLD_ID_LST}")
        if sld_id_lst is not None:
            for sld_id_elem in sld_id_lst.findall(Elements.SLD_ID):
                if sld_id_elem.get(Attributes.ID) == str(slide_id):
                    sld_id_lst.remove(sld_id_elem)
                    break

        return True

    def get_slide_size(self) -> tuple[int, int]:
        """
        Get the slide size in EMUs (English Metric Units).

        Returns:
            Tuple of (width, height) in EMUs.
        """
        sld_sz = self._root.find(f".//{Elements.SLD_SZ}")
        if sld_sz is not None:
            cx = int(sld_sz.get(Attributes.CX, '9144000'))  # Default: 10 inches
            cy = int(sld_sz.get(Attributes.CY, '6858000'))  # Default: 7.5 inches
            return (cx, cy)
        return (9144000, 6858000)  # Default widescreen

    def get_notes_size(self) -> tuple[int, int]:
        """
        Get the notes slide size in EMUs.

        Returns:
            Tuple of (width, height) in EMUs.
        """
        notes_sz = self._root.find(f".//{Elements.NOTES_SZ}")
        if notes_sz is not None:
            cx = int(notes_sz.get(Attributes.CX, '6858000'))
            cy = int(notes_sz.get(Attributes.CY, '9144000'))
            return (cx, cy)
        return (6858000, 9144000)  # Default portrait

    def set_notes_size(self, cx: int, cy: int) -> None:
        """
        Set the notes slide size in EMUs.

        Args:
            cx: Width in EMUs.
            cy: Height in EMUs.
        """
        notes_sz = self._root.find(f".//{Elements.NOTES_SZ}")
        if notes_sz is not None:
            notes_sz.set(Attributes.CX, str(cx))
            notes_sz.set(Attributes.CY, str(cy))
        else:
            # Insert after sldSz if present, otherwise append
            notes_sz = ET.Element(Elements.NOTES_SZ)
            notes_sz.set(Attributes.CX, str(cx))
            notes_sz.set(Attributes.CY, str(cy))
            sld_sz = self._root.find(f".//{Elements.SLD_SZ}")
            if sld_sz is not None:
                idx = list(self._root).index(sld_sz)
                self._root.insert(idx + 1, notes_sz)
            else:
                self._root.append(notes_sz)

    def get_first_slide_number(self) -> int:
        """Get the first slide number for numbering."""
        return int(self._root.get('firstSlideNum', '1'))

    def set_first_slide_number(self, number: int) -> None:
        """Set the first slide number for numbering."""
        self._root.set('firstSlideNum', str(number))

    def save(self) -> None:
        """Save the presentation.xml back to the package."""
        xml_bytes = ET.tostring(
            self._root,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8',
            standalone=True
        )
        self._package.set_part(self.PART_NAME, xml_bytes)

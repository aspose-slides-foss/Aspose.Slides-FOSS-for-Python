"""
Content Types management for OPC packages.

Handles [Content_Types].xml which maps file extensions and specific parts
to their MIME content types.
"""

from __future__ import annotations
import lxml.etree as ET
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .opc_package import OpcPackage

# Content Types namespace
CT_NAMESPACE = "http://schemas.openxmlformats.org/package/2006/content-types"
CT_NS = f"{{{CT_NAMESPACE}}}"

# Common PPTX content types
CONTENT_TYPES = {
    'presentation': 'application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml',
    'presentation_macro': 'application/vnd.ms-powerpoint.presentation.macroEnabled.main+xml',
    'slide': 'application/vnd.openxmlformats-officedocument.presentationml.slide+xml',
    'slide_layout': 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml',
    'slide_master': 'application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml',
    'notes_slide': 'application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml',
    'notes_master': 'application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml',
    'handout_master': 'application/vnd.openxmlformats-officedocument.presentationml.handoutMaster+xml',
    'theme': 'application/vnd.openxmlformats-officedocument.theme+xml',
    'core_properties': 'application/vnd.openxmlformats-package.core-properties+xml',
    'extended_properties': 'application/vnd.openxmlformats-officedocument.extended-properties+xml',
    'chart': 'application/vnd.openxmlformats-officedocument.drawingml.chart+xml',
    'chartsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.chartsheet+xml',
    'comments': 'application/vnd.openxmlformats-officedocument.presentationml.comments+xml',
    'commentAuthors': 'application/vnd.openxmlformats-officedocument.presentationml.commentAuthors+xml',
}


class ContentTypesManager:
    """
    Manages the [Content_Types].xml file in an OPC package.

    This class provides methods to:
    - Parse existing content types
    - Add overrides for specific parts
    - Add default extensions
    - Serialize back to XML
    """

    PART_NAME = '[Content_Types].xml'

    def __init__(self, package: OpcPackage):
        """
        Initialize the content types manager.

        Args:
            package: The OPC package to manage content types for.
        """
        self._package = package
        self._root: Optional[ET._Element] = None
        self._load()

    def _load(self) -> None:
        """Load and parse the [Content_Types].xml from the package."""
        content = self._package.get_part(self.PART_NAME)
        if content:
            self._root = ET.fromstring(content)
        else:
            # Create minimal content types structure
            self._root = ET.Element(f"{CT_NS}Types")
            self._add_default_extension('rels', 'application/vnd.openxmlformats-package.relationships+xml')
            self._add_default_extension('xml', 'application/xml')

    def _add_default_extension(self, extension: str, content_type: str) -> None:
        """Add a default content type mapping for a file extension."""
        default = ET.SubElement(self._root, f"{CT_NS}Default")
        default.set('Extension', extension)
        default.set('ContentType', content_type)

    def add_override(self, part_name: str, content_type: str) -> None:
        """
        Add a content type override for a specific part.

        Args:
            part_name: The part path (e.g., '/ppt/slides/slide1.xml').
            content_type: The MIME content type.
        """
        # Ensure part_name starts with /
        if not part_name.startswith('/'):
            part_name = '/' + part_name

        # Check if override already exists
        for override in self._root.findall(f"{CT_NS}Override"):
            if override.get('PartName') == part_name:
                override.set('ContentType', content_type)
                return

        # Add new override
        override = ET.SubElement(self._root, f"{CT_NS}Override")
        override.set('PartName', part_name)
        override.set('ContentType', content_type)

    def remove_override(self, part_name: str) -> bool:
        """
        Remove a content type override for a specific part.

        Args:
            part_name: The part path.

        Returns:
            True if override was removed, False if it didn't exist.
        """
        if not part_name.startswith('/'):
            part_name = '/' + part_name

        for override in self._root.findall(f"{CT_NS}Override"):
            if override.get('PartName') == part_name:
                self._root.remove(override)
                return True
        return False

    def get_content_type(self, part_name: str) -> Optional[str]:
        """
        Get the content type for a specific part.

        Args:
            part_name: The part path.

        Returns:
            Content type string or None if not found.
        """
        if not part_name.startswith('/'):
            part_name = '/' + part_name

        # Check overrides first
        for override in self._root.findall(f"{CT_NS}Override"):
            if override.get('PartName') == part_name:
                return override.get('ContentType')

        # Fall back to defaults based on extension
        ext = part_name.rsplit('.', 1)[-1] if '.' in part_name else ''
        for default in self._root.findall(f"{CT_NS}Default"):
            if default.get('Extension') == ext:
                return default.get('ContentType')

        return None

    def save(self) -> None:
        """Save the content types back to the package."""
        # Re-indent to ensure consistent formatting after adding new elements
        ET.indent(self._root, space='  ')

        xml_bytes = ET.tostring(
            self._root,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8',
            standalone=True
        )
        self._package.set_part(self.PART_NAME, xml_bytes)

"""
PPTX format exporter.

Exports presentations to PPTX (and related) formats by saving
the OPC package directly.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, BinaryIO, Optional, Any

from .exporter_base import ExporterBase
from .exporter_registry import ExporterRegistry
from ..opc.content_types import ContentTypesManager

if TYPE_CHECKING:
    from ..opc import OpcPackage


class PptxExporter(ExporterBase):
    """
    Exporter for PPTX and related Office Open XML formats.

    Supports:
    - PPTX: Standard PowerPoint presentation
    - PPTM: Macro-enabled presentation
    - PPSX: PowerPoint show (opens in slideshow mode)
    - PPSM: Macro-enabled show
    - POTX: PowerPoint template
    - POTM: Macro-enabled template

    These formats are all OPC packages with different content types
    for the main presentation part.
    """

    # Mapping from SaveFormat values to main presentation content types
    _CONTENT_TYPES = {
        'Pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml',
        'Pptm': 'application/vnd.ms-powerpoint.presentation.macroEnabled.main+xml',
        'Ppsx': 'application/vnd.openxmlformats-officedocument.presentationml.slideshow.main+xml',
        'Ppsm': 'application/vnd.ms-powerpoint.slideshow.macroEnabled.main+xml',
        'Potx': 'application/vnd.openxmlformats-officedocument.presentationml.template.main+xml',
        'Potm': 'application/vnd.ms-powerpoint.template.macroEnabled.main+xml',
    }

    #: The part whose content type identifies the package format.
    MAIN_PART_NAME = '/ppt/presentation.xml'

    def __init__(self, target_format: str = 'Pptx'):
        """
        Initialize the PPTX exporter.

        Args:
            target_format: The specific format to export to.

        Raises:
            ValueError: If the format is not one of the OPC presentation formats.
        """
        if target_format not in self._CONTENT_TYPES:
            raise ValueError(
                f"Export format '{target_format}' is not supported by this "
                f"exporter; it writes {', '.join(sorted(self._CONTENT_TYPES))}"
            )
        self._target_format = target_format

    @classmethod
    def create_for_format(cls, format_value: str) -> PptxExporter:
        """Create an exporter bound to a specific target format."""
        return cls(target_format=format_value)

    def export_to_path(
        self,
        package: OpcPackage,
        path: str,
        options: Optional[Any] = None
    ) -> None:
        """
        Export the presentation to a PPTX file.

        Args:
            package: The OPC package containing the presentation.
            path: The output file path.
            options: Optional ISaveOptions (currently unused for PPTX).
        """
        self._update_content_type_if_needed(package)
        package.save(path)

    def export_to_stream(
        self,
        package: OpcPackage,
        stream: BinaryIO,
        options: Optional[Any] = None
    ) -> None:
        """
        Export the presentation to a stream.

        Args:
            package: The OPC package containing the presentation.
            stream: The output stream.
            options: Optional ISaveOptions (currently unused for PPTX).
        """
        self._update_content_type_if_needed(package)
        package.save(stream)

    def _update_content_type_if_needed(self, package: OpcPackage) -> None:
        """
        Declare the target format in ``[Content_Types].xml``.

        The six OPC presentation formats share one package shape and differ
        only in the content type of ``/ppt/presentation.xml``.  Without this
        the package always claims to be an ordinary presentation, so a file
        saved as ``.potx`` or ``.ppsx`` contradicts its own extension and
        PowerPoint refuses to open it.
        """
        content_type = self._CONTENT_TYPES[self._target_format]

        content_types = ContentTypesManager(package)
        if content_types.get_content_type(self.MAIN_PART_NAME) == content_type:
            # Already correct; leave the part byte-for-byte alone.
            return
        content_types.add_override(self.MAIN_PART_NAME, content_type)
        content_types.save()

    @classmethod
    def get_supported_formats(cls) -> list[str]:
        """Get all OPC-based presentation formats."""
        return list(cls._CONTENT_TYPES.keys())


# Register the PPTX exporter for all supported formats
ExporterRegistry.register(PptxExporter)

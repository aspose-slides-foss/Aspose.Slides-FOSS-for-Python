"""
PPTX format exporter.

Exports presentations to PPTX (and related) formats by saving
the OPC package directly.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, BinaryIO, Optional, Any

from .exporter_base import ExporterBase
from .exporter_registry import ExporterRegistry

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

    def __init__(self, target_format: str = 'Pptx'):
        """
        Initialize the PPTX exporter.

        Args:
            target_format: The specific format to export to.
        """
        self._target_format = target_format

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
        Update the content type of the main presentation part if converting.

        This is needed when saving as a different format than the source
        (e.g., saving a PPTX as POTX).
        """
        # TODO: Implement content type update when format conversion is needed
        # For now, we preserve the original content type
        pass

    @classmethod
    def get_supported_formats(cls) -> list[str]:
        """Get all OPC-based presentation formats."""
        return list(cls._CONTENT_TYPES.keys())


class PptxExporterFactory:
    """
    Factory for creating PPTX exporters with specific target formats.

    This allows the registry to create format-specific exporter instances.
    """

    @staticmethod
    def create_for_format(format_value: str) -> PptxExporter:
        """Create a PPTX exporter for a specific format."""
        return PptxExporter(target_format=format_value)


# Register the PPTX exporter for all supported formats
ExporterRegistry.register(PptxExporter)

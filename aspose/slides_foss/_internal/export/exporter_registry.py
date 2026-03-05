"""
Registry for presentation format exporters.

Provides a central registry for all available exporters, allowing
new formats to be added without modifying existing code.
"""

from __future__ import annotations
from typing import Type, Optional, TYPE_CHECKING

from .exporter_base import ExporterBase

if TYPE_CHECKING:
    pass


class ExporterRegistry:
    """
    Central registry for format exporters.

    This registry maintains a mapping from SaveFormat values to their
    corresponding exporter classes. New exporters can be registered
    dynamically, making it easy to add new export formats.

    Usage:
        # Register an exporter
        ExporterRegistry.register(PptxExporter)

        # Get an exporter for a format
        exporter = ExporterRegistry.get_exporter('Pptx')
        exporter.export(package, 'output.pptx')
    """

    _exporters: dict[str, Type[ExporterBase]] = {}

    @classmethod
    def register(cls, exporter_class: Type[ExporterBase]) -> None:
        """
        Register an exporter class for its supported formats.

        Args:
            exporter_class: The exporter class to register.
                           Must implement get_supported_formats().
        """
        for format_value in exporter_class.get_supported_formats():
            cls._exporters[format_value] = exporter_class

    @classmethod
    def unregister(cls, format_value: str) -> bool:
        """
        Unregister an exporter for a specific format.

        Args:
            format_value: The SaveFormat value string to unregister.

        Returns:
            True if unregistered, False if not found.
        """
        if format_value in cls._exporters:
            del cls._exporters[format_value]
            return True
        return False

    @classmethod
    def get_exporter(cls, format_value: str) -> Optional[ExporterBase]:
        """
        Get an exporter instance for a specific format.

        Args:
            format_value: The SaveFormat value string (e.g., 'Pptx', 'Pdf').

        Returns:
            Exporter instance or None if no exporter is registered.
        """
        exporter_class = cls._exporters.get(format_value)
        if exporter_class:
            return exporter_class()
        return None

    @classmethod
    def get_exporter_class(cls, format_value: str) -> Optional[Type[ExporterBase]]:
        """
        Get the exporter class for a specific format.

        Args:
            format_value: The SaveFormat value string.

        Returns:
            Exporter class or None if not registered.
        """
        return cls._exporters.get(format_value)

    @classmethod
    def is_format_supported(cls, format_value: str) -> bool:
        """
        Check if a format has a registered exporter.

        Args:
            format_value: The SaveFormat value string.

        Returns:
            True if an exporter is registered for this format.
        """
        return format_value in cls._exporters

    @classmethod
    def get_supported_formats(cls) -> list[str]:
        """
        Get all formats that have registered exporters.

        Returns:
            List of SaveFormat value strings.
        """
        return list(cls._exporters.keys())

    @classmethod
    def clear(cls) -> None:
        """Clear all registered exporters. Mainly for testing."""
        cls._exporters.clear()

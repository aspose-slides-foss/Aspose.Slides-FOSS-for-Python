"""
Extensible export system module.

Provides an abstract base for exporters and a registry system that allows
adding new export formats without modifying the core Presentation class.

To add a new export format:
1. Create a new exporter class inheriting from ExporterBase
2. Implement export_to_path, export_to_stream, and get_supported_formats
3. Call ExporterRegistry.register(YourExporterClass) or import it here
"""

from .exporter_base import ExporterBase
from .exporter_registry import ExporterRegistry

# Import exporters to trigger their auto-registration
from . import pptx_exporter  # Registers PPTX, PPTM, PPSX, PPSM, POTX, POTM

__all__ = ['ExporterBase', 'ExporterRegistry']

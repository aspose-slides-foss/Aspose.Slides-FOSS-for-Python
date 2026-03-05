"""
OPC (Open Packaging Conventions) handling module.

Provides classes for reading and writing OPC packages (ZIP archives)
used by Office Open XML formats like PPTX, XLSX, DOCX.
"""

from .opc_package import OpcPackage
from .content_types import ContentTypesManager
from .relationships import RelationshipsManager

__all__ = ['OpcPackage', 'ContentTypesManager', 'RelationshipsManager']

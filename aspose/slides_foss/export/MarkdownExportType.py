from __future__ import annotations
from enum import Enum

class MarkdownExportType(Enum):
    """Type of rendering document."""
    TEXT_ONLY = 'TextOnly'  # Render only text.

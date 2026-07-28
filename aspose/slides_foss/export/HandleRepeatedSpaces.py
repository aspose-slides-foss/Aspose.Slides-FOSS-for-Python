from __future__ import annotations
from enum import Enum

class HandleRepeatedSpaces(Enum):
    """Specifies how repeated regular space characters should be handled during Markdown export."""
    NONE = 'None'  # All spaces are preserved as regular space characters without any changes. No transformation is applied, and multiple consecutive spaces are exported as-is.
    ALTERNATE_SPACES_TO_NBSP = 'AlternateSpacesToNbsp'
    MULTIPLE_SPACES_TO_NBSP = 'MultipleSpacesToNbsp'

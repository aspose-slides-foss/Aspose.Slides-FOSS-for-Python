from __future__ import annotations
from enum import Enum

class NewLineType(Enum):
    """Type of new line that will be used in generated document."""
    WINDOWS = 'Windows'  # DOS & Windows OS new line - \\r\\n
    UNIX = 'Unix'  # Unix & Mac OS X new line - \\n
    MAC = 'Mac'  # Mac (OS 9) new line - \\r

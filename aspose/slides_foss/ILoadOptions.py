from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .IBlobManagementOptions import IBlobManagementOptions
    from .IFontSources import IFontSources
    from .IInterruptionToken import IInterruptionToken
    from .IResourceLoadingCallback import IResourceLoadingCallback
    from .ISpreadsheetOptions import ISpreadsheetOptions
    from .warnings.IWarningCallback import IWarningCallback
    from .LoadFormat import LoadFormat

class ILoadOptions(ABC):
    pass

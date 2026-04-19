from __future__ import annotations
from abc import ABC, abstractmethod

class IBaseShapeLock(ABC):
    """Represents Shape lock (disabled operation)."""
    @property
    @abstractmethod
    def no_locks(self) -> bool:
        """Return true if all lock-flags are disabled. Read-only ."""
        ...

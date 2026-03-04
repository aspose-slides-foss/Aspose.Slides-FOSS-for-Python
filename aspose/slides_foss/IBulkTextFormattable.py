from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload

class IBulkTextFormattable(ABC):
    """Represents an object with possibility of bulk setting child text elements' formats."""
    @overload
    def set_text_format(self, source) -> None:
        ...

    @overload
    def set_text_format(self, source) -> None:
        ...

    @overload
    def set_text_format(self, source) -> None:
        ...



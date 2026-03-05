from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, Any

class IImage(ABC):
    """Represents a raster or vector image."""
    @property
    def size(self) -> Any:
        """Gets the size of the image."""
        ...

    @property
    def width(self) -> int:
        """Gets the width of the image in pixels."""
        ...

    @property
    def height(self) -> int:
        """Gets the height of the image in pixels."""
        ...

    @overload
    def save(self, filename) -> None:
        ...

    @overload
    def save(self, filename, format) -> None:
        ...

    @overload
    def save(self, stream, format) -> None:
        ...

    @overload
    def save(self, filename, format, quality) -> None:
        ...

    @overload
    def save(self, stream, format, quality) -> None:
        ...



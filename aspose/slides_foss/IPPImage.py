from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING

if TYPE_CHECKING:
    from .IImage import IImage

class IPPImage(ABC):
    """Represents an image in a presentation."""
    @property
    def binary_data(self) -> list[int]:
        """Returns the copy of an image's data. Read-only []."""
        ...

    @property
    def image(self) -> IImage:
        """Returns the copy of an image. Read-only ."""
        ...



    @property
    def content_type(self) -> str:
        """Returns a MIME type of an image, encoded in . Read-only ."""
        ...

    @property
    def width(self) -> int:
        """Returns a width of an image. Read-only ."""
        ...

    @property
    def height(self) -> int:
        """Returns a height of an image. Read-only ."""
        ...

    @property
    def x(self) -> int:
        """Returns a X-offset of an image. Read-only ."""
        ...

    @property
    def y(self) -> int:
        """Returns a Y-offset of an image. Read-only ."""
        ...

    @overload
    def replace_image(self, new_image_data) -> None:
        ...

    @overload
    def replace_image(self, new_image) -> None:
        ...

    @overload
    def replace_image(self, new_image) -> None:
        ...



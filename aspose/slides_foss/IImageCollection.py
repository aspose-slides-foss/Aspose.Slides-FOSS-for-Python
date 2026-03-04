from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .IImage import IImage
    from .IPPImage import IPPImage

class IImageCollection(ABC):
    """Represents collection of PPImage."""
    @property
    def as_i_collection(self) -> list:
        ...

    @property
    def as_i_enumerable(self) -> Any:
        ...

    @overload
    def add_image(self, image) -> IPPImage:
        ...

    @overload
    def add_image(self, stream) -> IPPImage:
        ...

    @overload
    def add_image(self, stream, loading_stream_behavior) -> IPPImage:
        ...

    @overload
    def add_image(self, buffer) -> IPPImage:
        ...

    @overload
    def add_image(self, image_source) -> IPPImage:
        ...

    @overload
    def add_image(self, svg_image) -> IPPImage:
        ...
    def __getitem__(self, index: int) -> IImage:
        ...


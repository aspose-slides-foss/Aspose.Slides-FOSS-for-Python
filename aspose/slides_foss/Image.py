from __future__ import annotations
from typing import overload, TYPE_CHECKING, Union, BinaryIO
from .IImage import IImage

if TYPE_CHECKING:
    pass


class Image(IImage):
    """Represents a raster or vector image."""

    def _init_internal(self, data: bytes, content_type: str) -> None:
        """
        Internal initialization with image data.

        Args:
            data: Raw image bytes.
            content_type: MIME type of the image.
        """
        from ._internal.pptx.image_utils import get_image_dimensions
        self._data = data
        self._content_type = content_type
        self._width, self._height = get_image_dimensions(data)

    @property
    def size(self):
        """Gets the size of the image."""
        if not hasattr(self, '_data'):
            raise NotImplementedError("This feature is not yet available in this version.")
        return (self._width, self._height)

    @property
    def width(self) -> int:
        """Gets the width of the image in pixels."""
        if not hasattr(self, '_data'):
            raise NotImplementedError("This feature is not yet available in this version.")
        return self._width

    @property
    def height(self) -> int:
        """Gets the height of the image in pixels."""
        if not hasattr(self, '_data'):
            raise NotImplementedError("This feature is not yet available in this version.")
        return self._height






    def save(self, *args, **kwargs) -> None:
        if not hasattr(self, '_data'):
            raise NotImplementedError("This feature is not yet available in this version.")

        if len(args) < 1:
            raise TypeError("save() requires at least 1 argument")

        destination = args[0]

        if isinstance(destination, str):
            with open(destination, 'wb') as f:
                f.write(self._data)
        elif hasattr(destination, 'write'):
            destination.write(self._data)
        else:
            raise TypeError(f"Unsupported destination type: {type(destination)}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

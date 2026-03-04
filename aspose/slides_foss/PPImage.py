from __future__ import annotations
from typing import overload, TYPE_CHECKING, Optional
from .IPPImage import IPPImage

if TYPE_CHECKING:
    from .IImage import IImage
    from .ISvgImage import ISvgImage
    from ._internal.opc import OpcPackage

class PPImage(IPPImage):
    """Represents an image in a presentation."""

    def _init_internal(self, package: OpcPackage, part_name: str,
                       image_data: bytes, content_type: str) -> None:
        """
        Internal initialization with OPC package reference.

        Args:
            package: The OPC package containing the image.
            part_name: The part path (e.g., 'ppt/media/image1.jpg').
            image_data: Raw image bytes.
            content_type: MIME type of the image.
        """
        from ._internal.pptx.image_utils import get_image_dimensions
        self._package = package
        self._part_name = part_name
        self._image_data = image_data
        self._content_type = content_type
        self._width, self._height = get_image_dimensions(image_data)

    @property
    def binary_data(self) -> list[int]:
        """Returns the copy of an image's data. Read-only []."""
        if not hasattr(self, '_image_data'):
            raise NotImplementedError("This feature is not yet available in this version.")
        return list(self._image_data)

    @property
    def image(self) -> IImage:
        """Returns the copy of an image. Read-only ."""
        if not hasattr(self, '_image_data'):
            raise NotImplementedError("This feature is not yet available in this version.")
        from .Image import Image
        img = Image()
        img._init_internal(self._image_data, self._content_type)
        return img



    @property
    def content_type(self) -> str:
        """Returns a MIME type of an image, encoded in . Read-only ."""
        if not hasattr(self, '_content_type'):
            raise NotImplementedError("This feature is not yet available in this version.")
        return self._content_type

    @property
    def width(self) -> int:
        """Returns a width of an image. Read-only ."""
        if not hasattr(self, '_image_data'):
            raise NotImplementedError("This feature is not yet available in this version.")
        return self._width

    @property
    def height(self) -> int:
        """Returns a height of an image. Read-only ."""
        if not hasattr(self, '_image_data'):
            raise NotImplementedError("This feature is not yet available in this version.")
        return self._height

    @property
    def x(self) -> int:
        """Returns a X-offset of an image. Read-only ."""
        if not hasattr(self, '_image_data'):
            raise NotImplementedError("This feature is not yet available in this version.")
        return 0

    @property
    def y(self) -> int:
        """Returns a Y-offset of an image. Read-only ."""
        if not hasattr(self, '_image_data'):
            raise NotImplementedError("This feature is not yet available in this version.")
        return 0




    def replace_image(self, *args, **kwargs) -> None:
        if not hasattr(self, '_package'):
            raise NotImplementedError("This feature is not yet available in this version.")

        if len(args) < 1:
            raise TypeError("replace_image() requires at least 1 argument")

        from ._internal.pptx.image_utils import get_image_dimensions, guess_content_type

        arg = args[0]

        # Determine the new image data
        if isinstance(arg, (bytes, bytearray)):
            new_data = bytes(arg)
        elif isinstance(arg, list):
            # list[int] -> bytes
            new_data = bytes(arg)
        elif hasattr(arg, '_image_data'):
            # PPImage or similar
            new_data = arg._image_data
        elif hasattr(arg, '_data'):
            # Image object
            new_data = arg._data
        else:
            raise TypeError(f"Unsupported argument type: {type(arg)}")

        # Update the image data in the package
        self._image_data = new_data
        self._content_type = guess_content_type(new_data)
        self._width, self._height = get_image_dimensions(new_data)
        self._package.set_part(self._part_name, new_data)

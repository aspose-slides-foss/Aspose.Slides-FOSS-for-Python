from __future__ import annotations
import re
from typing import overload, TYPE_CHECKING, Any
from .IImageCollection import IImageCollection

if TYPE_CHECKING:
    from .Image import Image
    from .IPPImage import IPPImage
    from ._internal.opc import OpcPackage

class ImageCollection(IImageCollection):
    """Represents collection of PPImage."""

    def _init_internal(self, package: OpcPackage) -> None:
        """
        Internal initialization - scans the package for all images in ppt/media/.

        Args:
            package: The OPC package containing the presentation.
        """
        from .PPImage import PPImage
        from ._internal.pptx.image_utils import guess_content_type

        self._package = package
        self._images: list[PPImage] = []

        # Scan ppt/media/ for image files
        for part_name in sorted(package.get_part_names()):
            if part_name.startswith('ppt/media/'):
                image_data = package.get_part(part_name)
                if image_data:
                    content_type = guess_content_type(image_data)
                    pp_image = PPImage()
                    pp_image._init_internal(package, part_name, image_data, content_type)
                    self._images.append(pp_image)

    @property
    def as_i_collection(self) -> list:
        if not hasattr(self, '_images'):
            raise NotImplementedError("This feature is not yet available in this version.")
        return list(self._images)

    @property
    def as_i_enumerable(self) -> Any:
        if not hasattr(self, '_images'):
            raise NotImplementedError("This feature is not yet available in this version.")
        return iter(self._images)







    def add_image(self, *args, **kwargs) -> IPPImage:
        if not hasattr(self, '_package'):
            raise NotImplementedError("This feature is not yet available in this version.")

        if len(args) < 1:
            raise TypeError("add_image() requires at least 1 argument")

        from .PPImage import PPImage
        from ._internal.pptx.image_utils import (
            guess_content_type, guess_extension,
            EXTENSION_CONTENT_TYPES,
        )
        from ._internal.opc import ContentTypesManager

        arg = args[0]

        # Resolve the image data from the argument
        if isinstance(arg, (bytes, bytearray)):
            image_data = bytes(arg)
        elif isinstance(arg, list):
            # list[int] -> bytes
            image_data = bytes(arg)
        elif hasattr(arg, 'read'):
            # Stream-like object
            image_data = arg.read()
            if not isinstance(image_data, bytes):
                image_data = image_data.encode('utf-8')
        elif hasattr(arg, '_image_data'):
            # PPImage
            image_data = arg._image_data
        elif hasattr(arg, '_data'):
            # Image object
            image_data = arg._data
        else:
            raise TypeError(f"Unsupported argument type for add_image: {type(arg)}")

        # Check for duplicate images (same binary data)
        for existing in self._images:
            if existing._image_data == image_data:
                return existing

        # Determine content type and extension
        content_type = guess_content_type(image_data)
        extension = guess_extension(image_data)

        # Find the next available image number
        next_num = self._find_next_image_number()

        # Create the part name
        part_name = f'ppt/media/image{next_num}.{extension}'

        # Store the image in the package
        self._package.set_part(part_name, image_data)

        # Ensure the default extension content type is registered
        ct_manager = ContentTypesManager(self._package)
        if extension in EXTENSION_CONTENT_TYPES:
            # Check if this default extension already exists
            existing_ct = ct_manager.get_content_type(f'dummy.{extension}')
            if existing_ct is None:
                ct_manager._add_default_extension(extension, EXTENSION_CONTENT_TYPES[extension])
                ct_manager.save()

        # Create and track the PPImage
        pp_image = PPImage()
        pp_image._init_internal(self._package, part_name, image_data, content_type)
        self._images.append(pp_image)

        return pp_image

    def _find_next_image_number(self) -> int:
        """Find the next available image number in ppt/media/."""
        existing_numbers: set[int] = set()
        for part_name in self._package.get_part_names():
            if part_name.startswith('ppt/media/'):
                match = re.match(r'ppt/media/image(\d+)\.', part_name)
                if match:
                    existing_numbers.add(int(match.group(1)))

        num = 1
        while num in existing_numbers:
            num += 1
        return num

    def __getitem__(self, index: int) -> Image:
        if not hasattr(self, '_images'):
            raise NotImplementedError("This feature is not yet available in this version.")
        return self._images[index]

    def __len__(self) -> int:
        if not hasattr(self, '_images'):
            return 0
        return len(self._images)

    def __iter__(self):
        if not hasattr(self, '_images'):
            return iter([])
        return iter(self._images)

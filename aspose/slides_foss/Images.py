from __future__ import annotations
from typing import overload, TYPE_CHECKING

if TYPE_CHECKING:
    from .IImage import IImage

class Images(object):
    """Methods to instantiate and work with ."""


    @staticmethod
    def from_file(*args, **kwargs) -> IImage:
        if len(args) < 1:
            raise TypeError("from_file() requires at least 1 argument")

        from .Image import Image
        from ._internal.pptx.image_utils import guess_content_type

        filename = args[0]
        with open(filename, 'rb') as f:
            data = f.read()

        content_type = guess_content_type(data)
        img = Image()
        img._init_internal(data, content_type)
        return img




    @staticmethod
    def from_stream(*args, **kwargs) -> IImage:
        if len(args) < 1:
            raise TypeError("from_stream() requires at least 1 argument")

        from .Image import Image
        from ._internal.pptx.image_utils import guess_content_type

        stream = args[0]
        data = stream.read()
        if not isinstance(data, bytes):
            data = data.encode('utf-8')

        content_type = guess_content_type(data)
        img = Image()
        img._init_internal(data, content_type)
        return img

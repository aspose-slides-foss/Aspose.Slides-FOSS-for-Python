from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from .effects.IImageTransformOperationCollection import IImageTransformOperationCollection
    from .IPPImage import IPPImage

class ISlidesPicture(ISlideComponent, IPresentationComponent, ABC):
    """Represents a picture in a presentation."""
    @property
    def image(self) -> IPPImage:
        """Returns or sets the embedded image. Read/write ."""
        ...

    @image.setter
    def image(self, value: IPPImage):
        ...

    @property
    def link_path_long(self) -> str:
        """Returns of sets linked image's URL. Read/write ."""
        ...

    @link_path_long.setter
    def link_path_long(self, value: str):
        ...


    @property
    def as_i_slide_component(self) -> ISlideComponent:
        """Allows to get base ISlideComponent interface. Read-only ."""
        ...

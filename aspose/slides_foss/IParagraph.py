from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from .IParagraphFormat import IParagraphFormat
    from .IPortionCollection import IPortionCollection
    from .IPortionFormat import IPortionFormat

class IParagraph(ISlideComponent, IPresentationComponent, ABC):
    """Represents a paragraph of a text."""
    @property
    def portions(self) -> IPortionCollection:
        """Returns the collection of a text portions. Read-only ."""
        ...

    @property
    def paragraph_format(self) -> IParagraphFormat:
        """Returns the formatting object for this paragraph. Read-only ."""
        ...

    @property
    def text(self) -> str:
        """Gets or sets the the plain text of a paragraph. Read/write ."""
        ...

    @text.setter
    def text(self, value: str):
        ...



    @property
    def as_i_slide_component(self) -> ISlideComponent:
        """Allows to get base ISlideComponent interface. Read-only ."""
        ...




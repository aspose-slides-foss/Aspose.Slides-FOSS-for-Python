from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from .ICell import ICell
    from .IParagraphCollection import IParagraphCollection
    from .IShape import IShape
    from .ITextFrameFormat import ITextFrameFormat

class ITextFrame(ISlideComponent, IPresentationComponent, ABC):
    """Represents a TextFrame."""
    @property
    def paragraphs(self) -> IParagraphCollection:
        """Returns the list of all paragraphs in a frame. Read-only ."""
        ...

    @property
    def text(self) -> str:
        """Gets or sets the plain text for a TextFrame. Read/write ."""
        ...

    @text.setter
    def text(self, value: str):
        ...

    @property
    def text_frame_format(self) -> ITextFrameFormat:
        """Returns the formatting object for this TextFrame object. Read-only ."""
        ...


    @property
    def parent_shape(self) -> IShape:
        """Returns the parent shape or null if the parent object does not implement the IShape interface Read-only ."""
        ...

    @property
    def parent_cell(self) -> ICell:
        """Returns the parent cell or null if the parent object does not implement the ICell interface. Read-only ."""
        ...

    @property
    def as_i_slide_component(self) -> ISlideComponent:
        """Allows to get base ISlideComponent interface. Read-only ."""
        ...












from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING, Any
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from .IPortionFormat import IPortionFormat

class IPortion(ISlideComponent, IPresentationComponent, ABC):
    """Represents a portion of text inside a text paragraph."""
    @property
    def portion_format(self) -> IPortionFormat:
        """Returns formatting object which contains explicitly set formatting properties of the text portion with no inheritance applied. Read-only ."""
        ...

    @property
    def text(self) -> str:
        """Gets or sets the plain text of a portion. Read/write ."""
        ...

    @text.setter
    def text(self, value: str):
        ...


    @property
    def as_i_slide_component(self) -> ISlideComponent:
        """Allows to get base ISlideComponent interface. Read-only ."""
        ...







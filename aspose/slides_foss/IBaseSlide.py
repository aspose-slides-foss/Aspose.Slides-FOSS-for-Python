from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .theme.IThemeable import IThemeable
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from .IAnimationTimeLine import IAnimationTimeLine
    from .IBackground import IBackground
    from .IControlCollection import IControlCollection
    from .ICustomData import ICustomData
    from .IHyperlinkQueries import IHyperlinkQueries
    from .IShape import IShape
    from .IShapeCollection import IShapeCollection
    from .ISlideShowTransition import ISlideShowTransition

class IBaseSlide(IThemeable, ISlideComponent, IPresentationComponent, ABC):
    """Represents common data for all slide types."""
    @property
    def shapes(self) -> IShapeCollection:
        """Returns the shapes of a slide. Read-only ."""
        ...


    @property
    def name(self) -> str:
        """Returns or sets the name of a slide. Read/write ."""
        ...

    @name.setter
    def name(self, value: str):
        ...

    @property
    def slide_id(self) -> int:
        """Returns the ID of a slide. Read-only ."""
        ...












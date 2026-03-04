from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from ..ISlideComponent import ISlideComponent
from ..IPresentationComponent import IPresentationComponent

if TYPE_CHECKING:
    from ..IBaseSlide import IBaseSlide
    from ..IPresentation import IPresentation
    from .IThemeEffectiveData import IThemeEffectiveData

class IThemeable(ISlideComponent, IPresentationComponent, ABC):
    """Represents objects that can be themed with ."""



    @property
    def presentation(self) -> IPresentation:
        ...



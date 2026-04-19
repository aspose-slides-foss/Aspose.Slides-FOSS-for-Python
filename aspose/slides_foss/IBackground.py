from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .ISlideComponent import ISlideComponent
from .IPresentationComponent import IPresentationComponent
from .IFillParamSource import IFillParamSource

if TYPE_CHECKING:
    from .BackgroundType import BackgroundType
    from .IBackgroundEffectiveData import IBackgroundEffectiveData
    from .IColorFormat import IColorFormat
    from .IEffectFormat import IEffectFormat
    from .IFillFormat import IFillFormat

class IBackground(ISlideComponent, IPresentationComponent, IFillParamSource, ABC):
    """Represents background of a slide."""
    @property
    @abstractmethod
    def type(self) -> BackgroundType:
        ...

    @type.setter
    @abstractmethod
    def type(self, value: BackgroundType):
        ...

    @property
    @abstractmethod
    def fill_format(self) -> IFillFormat:
        ...

    @property
    @abstractmethod
    def effect_format(self) -> IEffectFormat:
        ...

    @property
    @abstractmethod
    def style_color(self) -> IColorFormat:
        ...

    @property
    @abstractmethod
    def style_index(self) -> int:
        ...

    @style_index.setter
    @abstractmethod
    def style_index(self, value: int):
        ...

    @property
    @abstractmethod
    def as_i_slide_component(self) -> ISlideComponent:
        ...

    @property
    @abstractmethod
    def as_i_fill_param_source(self) -> IFillParamSource:
        ...

    @abstractmethod
    def get_effective(self) -> IBackgroundEffectiveData:
        ...

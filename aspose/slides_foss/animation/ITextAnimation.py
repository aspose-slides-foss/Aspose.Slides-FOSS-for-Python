from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .BuildType import BuildType
    from .IEffect import IEffect

class ITextAnimation(ABC):
    """Represent text animation."""
    @property
    @abstractmethod
    def build_type(self) -> BuildType:
        """List of build type (for exp. Paragraph 1,2,3, All at Once) of text animation. Read/write ."""
        ...
    @build_type.setter
    @abstractmethod
    def build_type(self, value: BuildType):
        ...
    @property
    @abstractmethod
    def effect_animate_background_shape(self) -> IEffect:
        """Linked shape effect with group or not (null) Read/write ."""
        ...
    @effect_animate_background_shape.setter
    @abstractmethod
    def effect_animate_background_shape(self, value: IEffect):
        ...
    @abstractmethod
    def add_effect(self, effect_type, subtype, trigger_type) -> IEffect:
        ...